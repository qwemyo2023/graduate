import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
from flask import Flask, render_template, request
#connect

host_name = 'localhost'
host_port = 3306
username = 'root'
password = '1234'
database_name = 'fooddb'
#DB connection 실행
def food_list(food_name):

    food_db = pymysql.connect(
    host=host_name,
    port=host_port,
    user=username,
    passwd=password,
    db=database_name,
    charset='utf8'
)
    #Cursor 생성
    cursor = food_db.cursor()

    #SQL문 실행
    sql = f"""
                SELECT food, serv, cal, tan, dan, gee
                FROM foodtb
                WHERE food = '{food_name}'
                """
    cursor.execute(sql)
    #SQL 검색결과 가져오기

    rows = cursor.fetchall()
    print(rows)

    # price = []
    list = []
    for row in rows:
        print(list)
        list.append(row)
# DB connection 닫기
    food_db.close()
    return list

if __name__ == '__main__':
    arr = food_list(food_name)
    #arr = food_list(food)
    arr = np.array(arr)
    print(arr)
#df = pd.read_sql(SQL, db)
#df.to_csv('fooddb.csv', sep=',', index=False, encoding='utf-8')
#참고로 pandas 라이브러리의 read_sql() 함수는 첫 번째 인자로 SQL 쿼리를 받고, 두 번째 인자로 db connection객체를 받는다.