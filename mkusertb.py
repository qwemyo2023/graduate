#회원가입 user 정보 입력
import numpy as np
import pymysql
from sqlalchemy import create_engine
from flask import Flask, render_template, request
import json
from decimal import Decimal
from datetime import datetime
#connect
#userdb.usertb
#email, PW, MFM
host_name = 'localhost'
host_port = 3306
username = 'root'
password = '1234'
database_name = 'userdb'
#변수 > 전역사용가능한넘. 지역사용가능한넘.

def mysql_conn():
    return db_connection
def db_connection():
    conn = pymysql.connect(
    host=host_name,
    port=host_port,
    user=username,
    passwd=password,
    db=database_name,
    charset='utf8'
    )
    return conn

#DB connection 실행
def signup_process(email, password, gender, height, activity):

    conn = db_connection()
    #Cursor 생성
    #회원가입db(userdb.usertb)에 회원 추가하기
    cursor = conn.cursor()
    #sql=f"INSERT INTO tb_user(email, pwd, gender)VALUES(email, password, gender);"
    insert_sql = f"INSERT INTO tb_user (email, pwd, gender, height, activity) VALUES ('{email}', '{password}', '{gender}','{height}','{activity}')"
    print(insert_sql)
    insert_result=""
    cursor.execute(insert_sql)
    conn.commit()
    # height 변수를 정수로 변환
    height = int(height)
        # 표준 체중 계산
        #키를 cm->m변환
    m2 = height / 100
    if gender == 'M':
        e = m2 * m2 * 22
    else:
        e = m2 * m2 * 21

        # 표준 체중을 데이터베이스에 업데이트
    update_sql = f"UPDATE tb_user SET standard_weight = {e} WHERE email = '{email}'"
    cursor.execute(update_sql)
    conn.commit()

    print("사용자의 표준체중은", e, "kg입니다")
    #user_insert_cursor.execute(insert_query)
    #mkuserdb(email)
    try:
        # 예외가 발생할 가능성이 있는 코드
        insert_result = cursor.execute(insert_sql)
        conn.commit()
    except Exception as e:
        # 모든 예외를 문자열로 출력
        exception_str = str(e)
        insert_result = -1
        print(f"예외 발생: {exception_str}")

    conn.close()

    return insert_result


def user_login(user_id):
    conn = db_connection()
    user_cur = conn.cursor()
    if request.method == 'POST':
        login_info = request.form
        username = login_info['email']
        password = login_info['password']

        sql = "SELECT * FROM userdb WHERE email=%s"
        rows_count = user_cur.execute(sql, email=username)

        if rows_count >0:
            user_info =user_cur.fetchone()
            print("user info: ", user_info)

            is_pw_correct = user_info[2]
            print("password check: ", is_pw_correct)
            return render_template('login.html',info=user_info)

        else:
            print('user does not exist')
            return render_template('login.html',info='user does not exist')

        #return redirect(request.url)
    return render_template('MNCD_main1.html')

def search_login(email_input, password):
    conn = db_connection()
    cussor = conn.cursor()
    #tb_user에서 email주소가 같은 애를 고르겠다
    sql = f"SELECT email FROM tb_user WHERE email ='{email_input}' and pwd ='{password}'"
    #만약 email이 tb_user에 없다면?
    print("sql : ", sql)
    cussor.execute(sql)
    rows = cussor.fetchall()
    login_result = ""
    if len(rows)==0:
        login_result = "-1"
        print(rows)
    else:
        login_result = "1"
        print(rows)

    print("rows count : " , len(rows))


    return login_result

#세션에 있는 이메일(키)를 넣는다.
def add_food(food_name, flist, email):
    conn = db_connection()
    cursor = conn.cursor()
    foodinfo = [(f'"{flist[0][0]}"', *flist[0][1:])]

    # tb_personal 테이블에 데이터 추가
    sql = "INSERT INTO tb_personal (foodname, foodinfo, email) VALUES (%s, %s, %s)"
    cursor.execute(sql, (food_name, str(flist), email))

    # size, kcal, tan, dan, gee 값을 각각 변수에 저장
    size = flist[0][1]
    kcal = flist[0][2]
    tan = flist[0][3]
    dan = flist[0][4]
    gee = flist[0][5]

    # 각각의 값을 tb_personal 테이블에 업데이트
    update_sql = "UPDATE tb_personal SET size = %s, kcal = %s, tan = %s, dan = %s, gee = %s WHERE foodname = %s AND email = %s"
    cursor.execute(update_sql, (size, kcal, tan, dan, gee, food_name, email))

    conn.commit()
    conn.close()
    add_result = ""
    return add_result


def my_record(email):
    conn = db_connection()
    cursor = conn.cursor()
    sql = f"SELECT foodinfo FROM tb_personal WHERE email ='{email}'"
    print(sql)
    a= cursor.execute(sql)
    print(a)
    rows = cursor.fetchall()
    print(rows)

    record_list = []
    for row in rows:
        record_list.append(row)
    ###
    record_list = record_list[0]
    return record_list

def get_recent_records(email, limit=5):
    conn = db_connection()
    cursor = conn.cursor()
    sql = f"SELECT foodname, mealtime, size, kcal, tan, dan, gee FROM tb_personal WHERE email = '{email}' AND mealtime IS NOT NULL ORDER BY create_dt DESC LIMIT {limit};"
    cursor.execute(sql)
    rows = cursor.fetchall()
    record_list = [row for row in rows]

    return record_list


#사용자의 하루 최소 필요 열량 계산기
def calc_need_kcal(email):
    conn = db_connection()
    cursor = conn.cursor()
    sql = f"SELECT activity, standard_weight FROM tb_user WHERE email = '{email}';"
    cursor.execute(sql)
    result = cursor.fetchone()

    if result is not None:
        activity, standard_weight = result  # 결과에서 activity와 standard_weight를 가져와라
        print("activity:", activity)
        print("standard_weight:", standard_weight)
        if standard_weight is not None:
            try:
                standard_weight = float(standard_weight)  # 문자열-> 소수점
                if activity == 1:
                    s1 = standard_weight * 25
                    print("사용자의 최소 하루 필요 열량은", s1, "kcal입니다")
                    return s1
                elif activity == 2:
                    s1 = standard_weight * 30
                    print("사용자의 최소 하루 필요 열량은", s1, "kcal입니다")
                    return s1
                elif activity == 3:
                    s1 = standard_weight * 35
                    print("사용자의 최소 하루 필요 열량은", s1, "kcal입니다")
                    return s1
                elif activity == 4:
                    s1 = standard_weight * 40
                    print("사용자의 최소 하루 필요 열량은", s1, "kcal입니다")
                    return s1
                else:
                    print("올바른 활동량을 선택해 주세요")
                    return None
            except ValueError:
                print("키 정보가 숫자로 변환할 수 없습니다.")
                return None
        else:
            print("사용자의 키 정보가 없습니다.")
            return None
    else:
        print("사용자를 찾을 수 없습니다.")
        return None

##섭취 칼로리 토탈(날짜별)
def calc_total_kcal(email):
    conn = db_connection()
    cursor = conn.cursor()
    #kcal 불러오기, email 세션이 동일한 것에서, date가 같은 걸로
    sql = f"SELECT DATE(create_dt) AS date, SUM(kcal) AS total_kcal FROM tb_personal WHERE email = '{email}' GROUP BY DATE(create_dt);"
    print(sql)
    cursor.execute(sql)
    total_kcal_records = cursor.fetchall()  # 모든 결과 가져오기

    return total_kcal_records

##칼로리 비교
def compare_kcal(total, s1):
    #total=calc_total_kcal.total_kcal_records
    #s1 = calc_need_kcal.s1
    # total_records에서 최신 합산 Kcal 값을 추출
    if total:
        total_kcal_values = [record[1] for record in total]
        todays_total_v = max(total_kcal_values)

        if isinstance(s1, float):
            s1 = Decimal(str(s1))  # s1을 Decimal로 변환

        if s1 > todays_total_v:
            r = s1 - todays_total_v
            print("1일 권장 칼로리의 양은", s1, "이며,", r, "kcal 남았습니다")
            return s1, r
        elif s1 == todays_total_v:
            print("1일 권장 칼로리를 모두 섭취하셨습니다")
        else:
            o = todays_total_v - s1
            print("1일 권장 칼로리를", o, "kcal 넘으셨습니다")
            return o
    else:
        print("날짜별 Kcal 합산이 없습니다.")
        return None
def standard_w(email):
    conn = db_connection()
    cursor = conn.cursor()
    sql = f"SELECT standard_weight FROM tb_user WHERE email = '{email}';"
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    if rows:
        return rows[0][0]
    else:
        return None

##오늘 토탈 먹은거
def total_today(email):
    conn = db_connection()
    cursor = conn.cursor()
    #kcal 불러오기, email 세션이 동일한 것에서, date가 같은 걸로
    local_date = datetime.now().strftime('%Y-%m-%d')

    sql = f"SELECT SUM(kcal) AS total_kcal FROM tb_personal WHERE email = '{email}' AND DATE(create_dt) = '{local_date}';"
    print(sql)
    cursor.execute(sql)
    today_total_kcal_records = cursor.fetchall()  # 모든 결과 가져오기

    return today_total_kcal_records


##mypage에서 칼로리 비교하기
def compare_on_mypage(activity, total, email):
    print("activity:", activity)
    conn = db_connection()
    cursor = conn.cursor()
    sql = f"SELECT standard_weight FROM tb_user WHERE email = '{email}';"
    print("cmp_omp의 sql",sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    print("cmp_omp의 sql result: ",result)
    if result is not None:
        standard_weight = result[0]  # 튜플의 첫 번째 요소를 가져옴
        print("standard_weight:", standard_weight)
        if standard_weight is not None:
            try:
                activity=int(activity)
                if activity == 1:
                    s1 = standard_weight * 25
                    print("1")
                    #("사용자의 최소 하루 필요 열량은 ", s1, "kg입니다")
                elif activity == 2:
                    s1 = standard_weight * 30
                    print("2")
                elif activity == 3:
                    s1 = standard_weight * 35
                    print("3")
                elif activity == 4:
                    s1 = standard_weight * 40
                    print("4")
                else:
                    print("올바른 활동량을 선택해 주세요")
                    return None

                print("사용자의 최소 하루 필요 열량은", s1, "kcal입니다")   #여까진 됐다.
                print("before float total:", total)
                if total is not None:
                    # 튜플의 첫 번째 요소에 접근하고, Decimal을 float로 변환
                    todays_total_v = float(total[0][0])
                    print("total is not None:",todays_total_v)
                else:
                    todays_total_v = 0.0
                print("s1:",s1)
                s1 = int(s1)
                print("변경 후 s1:", s1)
                if total is not None:
                    # total을 리스트로 변환

                    if s1 > todays_total_v:
                        r = s1 - todays_total_v
                        print("1일 권장 칼로리의 양은", s1, "이며,", r, "kcal 남았습니다")
                        return s1, r
                    elif s1 == todays_total_v:
                        print("1일 권장 칼로리를 모두 섭취하셨습니다")
                        return s1, todays_total_v
                    else:
                        o =todays_total_v- s1
                        print("1일 권장 칼로리를", o, "kcal 넘으셨습니다")
                        return o
                else:
                    print("날짜별 Kcal 합산이 없습니다.")
                    return None

            except ValueError:
                print("키 정보가 숫자로 변환할 수 없습니다.")
                return None
        else:
            print("사용자의 키 정보가 없습니다.")
            return None
    else:
        print("사용자를 찾을 수 없습니다.")
        return None



#dt를 그룹으로 묶기
def mk_mypg_record_group_dt(email,record_list):
    conn = db_connection()
    cursor = conn.cursor()

    sql_email =sql = f"SELECT foodinfo FROM tb_personal WHERE email ='{email}'"
    print(sql_email)
    a= cursor.execute(sql_email)
    print(a)

    rows = cursor.fetchall()
    print(rows)

    record_list = []
    for row in rows:
        record_list.append(row)

    sql = f"SELECT  foodinfo , GROUP_CONCAT (create_dt) FROM  tb_personal GROUP  BY  foodinfo  WHERE email ='{email}';"
    cursor.execute(sql)
    g_rows = cursor.fetchall()
    print(g_rows)

    group_record_list=[]
    for row in rows:
        group_record_list.append(g_rows)

    print(g_rows)
    return g_rows
#create_dt(모델에 돌린 시간)
#foodname(음식이름)
#foodinfo(음식 정보)
"""f_name=record_list[0][0]
    serv=record_list[0][1]
    tan=record_list[0][2]
    dan=record_list[0][3]
    gee=record_list[0][4]"""
#https://extbrain.tistory.com/56
#마이페이지에 들고 갈 것(g_rows, g_rows의 각각의 datetime 정의하고 )
#유저가 mealtime까지 입력한 정보 골라내기
def my_upload(email):
    conn = db_connection()
    cursor = conn.cursor()

    #my_record의 결과값 받기
    #유저가 전체 조회한 내용을 받은 거임
    #그럼 그 중에 mealtime에 값이 있는 것만 골라서 출력하기
    sql = f"SELECT foodinfo, GROUP_CONCAT(create_dt) FROM tb_personal WHERE email = '{email}' GROUP BY foodinfo;"
    print(sql)
    cursor.execute(sql)
    rows = cursor.fetchall(sql)
    print(rows)

    my_upload_record = []
    for row in rows:
        my_upload_record.append(row)

    return my_upload_record

def update_mealtime(email, mealtime):
    conn = db_connection()
    cursor = conn.cursor()
    sql = f"UPDATE tb_personal SET mealtime = '{mealtime}' WHERE create_dt = (SELECT MAX(create_dt) FROM tb_personal WHERE email = '{email}');"
    print(sql)
    affected_rows = cursor.execute(sql)  # 실행된 업데이트 쿼리의 결과로 영향 받은 행 수를 얻습니다.
    conn.commit()  # 변경 사항을 커밋합니다.
    print(f"Affected rows: {affected_rows}")

    return affected_rows