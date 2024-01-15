import numpy as np
import pymysql
from sqlalchemy import create_engine
from flask import Flask, render_template, request
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
    return conn#일반적으로 성인의 1일 권장 칼로리는 남성이 2,700kcal이고 여성은 2,000kcal

#div_kcal=input_kcal/2700
height = int(input("키를 입력해주세요 "))
m2 = height/100
#s = int(input("남성인지 여성인지 선택해 주세요(남성은 0, 여성은 1입니다)"))
def cal_ragular_weight(gender, email):
    sql= f"SELECT gender FROM tb_user WHERE email ='{email}';"
    if gender == M:
        e = m2 * m2 * 22
        print("사용자의 표준체중은 ", e, "kg입니다")
    else:
        e = m2 * m2 * 21
        print("사용자의 표준체중은 ", e, "kg입니다")

standard_weight = (height/100)*(height/100)*21
activity = int(input("활동량을 선택해주세요. 1: 가벼운 활동 2: 중등도 활동 3: 강한 활동 4: 아주 강한 활동"))

if activity == 1:
  s1 = e * 25
  print("사용자의 최소 하루 필요 열량은 ", s1, "kg입니다")
elif activity == 2:
  s1 = e * 30
  print("사용자의 최소 하루 필요 열량은 ", s1, "kg입니다")
elif activity == 3:
  s1 = e * 35
  print("사용자의 최소 하루 필요 열량은 ", s1, "kg입니다")
elif activity == 4:
  s1 = e * 40
  print("사용자의 최소 하루 필요 열량은 ", s1, "kg입니다")
else:
  print("올바른 활동량을 선택해 주세요")


total = int(input("오늘 하루 섭취한 칼로리를 입력해주세요: "))
if s1 > total:
  r = s1 - total
  print("1일 권장 칼로리의 양은 ", s1,"이며, ", r, "kcal 남았습니다")
elif s1 == total:
  print("1일 권장 칼로리를 모두 섭취하셨습니다")
else:
  o = total - s1
  print("1일 권장 칼로리를 ", o, "kcal 넘으셨습니다")