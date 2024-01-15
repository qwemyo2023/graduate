import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from urllib.parse import unquote

import keras
from tensorflow.python.keras.models import Model, Sequential
#from tensorflow.keras.apps.densenet import DenseNet201
from tensorflow.python.keras.layers import GlobalAveragePooling2D, MaxPooling2D
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization
from keras import regularizers
from keras.callbacks import ReduceLROnPlateau
from PIL import Image
import numpy as np
from skimage import transform
from flask import Flask, render_template, request, redirect, url_for, session
from flask import Blueprint
from flask import flash
views = Blueprint('views', __name__)
import sys
import pymysql.cursors
#from flaskext.mysql import MySQL

import modelgogilyu
import modelbab
import modelgug_tang
import modelgimchi, modelgita, modelhaesanmul,modelmilgalu,modeltteog,modelyachaelyu


from app.mod_dbconn import food_list
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


from app.mkusertb import signup_process,search_login,add_food,my_record,my_upload,get_recent_records,update_mealtime,calc_need_kcal,calc_total_kcal,compare_kcal,compare_on_mypage
from app.mkusertb import compare_on_mypage,total_today,standard_w
import matplotlib.pyplot as plt
import numpy as np
import pymysql

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

current_directory = os.path.dirname(os.path.abspath(__file__))
upload_folder = os.path.join(current_directory, 'static', 'img')
app.config['UPLOAD_FOLDER'] = upload_folder

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)


@app.route("/")
def MNCD_main1():
    email_to_ID = None
    email_to_domain = None
    if 'email' in session:
        print("session['email']", session['email'])
        email_session = session['email']
        take_parts=email_session.split('@')
        email_to_ID=take_parts[0]
        email_to_domain =take_parts[1]
        print("email_to_ID:",email_to_ID)
        print("email_to_domain:", email_to_domain)
    else:
        email_session = ""
    print("email_session", email_session)
    return render_template("MNCD_main1.html", email_response=email_session, ID=email_to_ID, email_add=email_to_domain)

#회원가입
@app.route('/signup_form', methods=['GET', 'POST'])
def signup_form():
    return render_template("signup_form.html")


#회원가입완료
@app.route('/signup_ok', methods=['GET', 'POST'])
def signup_ok():
#변수 : 그릇 용도가 다양하다. 숫자, 문자, 함수,ETC
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    height = request.form.get('height')
    activity = request.form.get('activity')
    gender = request.form.get('gender')
    # password1, password2 비교 : 서로 다르다면 /signup 으로 재이동
    # password1, password2 비교

    if password1 != password2:
        print("비밀번호가 다릅니다.")
        return "비밀번호가 다릅니다."
    else:
        signup_process(email, password1, gender, height, activity)
        return render_template("signup_clear.html")  # 회원가입 성공 페이지로 리디렉션


        #signup_process(email,password1,gender,height,activity)
    #print(result_value)
    #return render_template("signup_ok.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/login_confirm", methods=['GET', 'POST'])
def login_confirm():
    email = request.form.get('email_input')
    password = request.form.get('password')
    print("email :", email)
    if email is None:
        print("email 없음")
    else:
        print("email 확인 완료")
    #이메일이랑 패스워드를 입력 받았고
    login_result = search_login(email, password)
    #form method="post" action="{{url_for('login')}}" id="login-form"
    if login_result == "1":
        print("로그인 성공")
        session['email'] = email
        return redirect('/')
        #render_template("MNCD_main1.html")
    else:
        print("로그인 실패")
        session['email'] = ""
        return redirect(url_for('login'))
        #render_template("login.html")

#로그아웃
@app.route('/logout')
def logout():
    session.pop('email')
    return redirect('/')


@app.route("/category")
def category():
    return render_template("category.html")

@app.route("/bab")
def bab():
    return render_template("bab.html")


@app.route("/foodexpl")
def foodexpl():
    return render_template("foodexpl.html")


@app.route("/gimchi")
def gimchi():
    return render_template("gimchi.html")


@app.route("/gita")
def gita():
    return render_template("gita.html")


@app.route("/gogilyu")
def gogilyu():
    return render_template("gogilyu.html")


@app.route("/gug_tang")
def gug_tang():
    return render_template("gug_tang.html")


@app.route("/haesanmul")
def haesanmul():
    return render_template("haesanmul.html")


@app.route("/milgalu")
def milgalu():
    return render_template("milgalu.html")


@app.route("/MNCD_intro")
def MNCD_intro():
    return render_template("MNCD_intro.html")


@app.route("/tteog")
def tteog():
    return render_template("tteog.html")


@app.route("/yachaelyu")
def yachaelyu():
    return render_template("yachaelyu.html")

#foodexplcat
@app.route("/foodexpl_bab")
def foodexpl_bab():
    return render_template("foodexpl_bab.html")


@app.route("/foodexpl_gimchi")
def foodexpl_gimchi():
    return render_template("foodexpl_gimchi.html")


@app.route("/foodexpl_gita")
def foodexpl_gita():
    return render_template("foodexpl_gita.html")


@app.route("/foodexpl_gogilyu")
def foodexpl_gogilyu():
    return render_template("foodexpl_gogilyu.html")


@app.route("/foodexpl_gug_tang")
def foodexpl_gug_tang():
    return render_template("foodexpl_gug_tang.html")


@app.route("/foodexpl_haesanmul")
def foodexpl_haesanmul():
    return render_template("foodexpl_haesanmul.html")


@app.route("/foodexpl_milgalu")
def foodexpl_milgalu():
    return render_template("foodexpl_milgalu.html")

@app.route("/foodexpl_tteog")
def foodexpl_tteog():
    return render_template("foodexpl_tteog.html")

@app.route("/foodexpl_yachaelyu")
def foodexpl_yachaelyu():
    return render_template("foodexpl_yachaelyu.html")

###고기류 모델
@app.route("/upload_done_gogilyu", methods=["POST"])
def upload_done_gogilyu():
    uploaded_files = request.files["file"]

    original_name = uploaded_files.filename

    # 현재 디렉토리와 상대 경로를 합쳐서 저장 경로를 만듭니다.
    save_path = os.path.join(upload_folder, original_name)
    print(save_path,"haha")
    if os.path.exists(save_path):
        print("delete file")
        os.remove(save_path)
    uploaded_files.save(save_path)

    return redirect(url_for("model_gogilyu", filepath=save_path))

@app.route("/model_gogilyu", methods=["GET", "POST"])
def model_gogilyu():
    filepath = request.args.get('filepath', '')
    filepath = unquote(filepath)
    if os.path.exists(filepath):
        print(filepath, " exists!")
    else:
        print(filepath, " not exists!")

    img_path = filepath
    result = modelgogilyu.model_gogilyu(filepath)
    print(result)
    global food
    food=result["TOP1"]
    food_n = food
    flist = food_list(food_n)
    print("flist:",flist)
    email=session.get("email")
    ###
    add_food(food_n, flist ,email)
    width_value4=flist[0][1]
    width_value5=flist[0][2]
    width_value1=flist[0][3]
    width_value2=flist[0][4]
    width_value3=flist[0][5]
    return render_template('result2.html', foodlist = flist, food_name = food_n, img_p = img_path, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)
###여기까지

#모델 밥
@app.route("/upload_done_bab", methods=["POST"])
def upload_done_bab():
    uploaded_files = request.files["file"]

    original_name = uploaded_files.filename

    # 현재 디렉토리와 상대 경로를 합쳐서 저장 경로를 만듭니다.
    save_path = os.path.join(upload_folder, original_name)
    print(save_path,"haha")
    if os.path.exists(save_path):
        print("delete file")
        os.remove(save_path)
    uploaded_files.save(save_path)
    return redirect(url_for("model_bab", filepath=save_path))

@app.route("/model_bab", methods=["GET", "POST"])
def model_bab():
    filepath = request.args.get('filepath', '')
    filepath = unquote(filepath)
    if os.path.exists(filepath):
        print(filepath, " exists!")
    else:
        print(filepath, " not exists!")
    #img_path = f"app/static/img/1.jpg"
    img_path = filepath
    result = modelbab.model_bab(filepath)
    print(result)
    global food
    food=result["TOP1"]
    food_n = food
    flist = food_list(food_n)
    print("flist:",flist)
    email=session.get("email")
    #email,now_t,food_name, foodlist
    add_food(food_n, flist ,email)
    width_value4=flist[0][1]
    width_value5=flist[0][2]
    width_value1=flist[0][3]
    width_value2=flist[0][4]
    width_value3=flist[0][5]
    return render_template('result2.html', foodlist = flist, food_name = food_n, img_p = img_path, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)
###여기까지

###모델 국,탕
@app.route("/upload_done_gug_tang", methods=["POST"])
def upload_done_gug_tang():
    uploaded_files = request.files["file"]

    original_name = uploaded_files.filename

    # 현재 디렉토리와 상대 경로를 합쳐서 저장 경로를 만듭니다.
    save_path = os.path.join(upload_folder, original_name)
    print(save_path,"haha")
    if os.path.exists(save_path):
        print("delete file")
        os.remove(save_path)
    uploaded_files.save(save_path)

    return redirect(url_for("model_gug_tang", filepath=save_path))

@app.route("/model_gug_tang", methods=["GET", "POST"])
def model_gug_tang():
    filepath = request.args.get('filepath', '')
    filepath = unquote(filepath)
    if os.path.exists(filepath):
        print(filepath, " exists!")
    else:
        print(filepath, " not exists!")
    #img_path = f"app/static/img/1.jpg"
    img_path = filepath
    result = modelgug_tang.model_gug_tang(filepath)
    print(result)
    global food
    food=result["TOP1"]
    food_n = food
    flist = food_list(food_n)
    print("flist:",flist)
    email=session.get("email")
    #email,now_t,food_name, foodlist
    add_food(food_n, flist ,email)
    width_value4=flist[0][1]
    width_value5=flist[0][2]
    width_value1=flist[0][3]
    width_value2=flist[0][4]
    width_value3=flist[0][5]
    return render_template('result2.html', foodlist = flist, food_name = food_n, img_p = img_path, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)
###여기까지

###모델 김치
@app.route("/upload_done_gimchi", methods=["POST"])
def upload_done_gimchi():
    uploaded_files = request.files["file"]

    original_name = uploaded_files.filename

    # 현재 디렉토리와 상대 경로를 합쳐서 저장 경로를 만듭니다.
    save_path = os.path.join(upload_folder, original_name)
    print(save_path,"haha")
    if os.path.exists(save_path):
        print("delete file")
        os.remove(save_path)
    uploaded_files.save(save_path)

    return redirect(url_for("model_gimchi", filepath=save_path))

@app.route("/model_gimchi", methods=["GET", "POST"])
def model_gimchi():
    filepath = request.args.get('filepath', '')
    filepath = unquote(filepath)
    if os.path.exists(filepath):
        print(filepath, " exists!")
    else:
        print(filepath, " not exists!")
    #img_path = f"app/static/img/1.jpg"
    img_path = filepath
    result = modelgimchi.model_gimchi(filepath)
    print(result)
    global food
    food=result["TOP1"]
    food_n = food
    flist = food_list(food_n)
    print("flist:",flist)
    email=session.get("email")
    #email,now_t,food_name, foodlist
    add_food(food_n, flist ,email)
    width_value4=flist[0][1]
    width_value5=flist[0][2]
    width_value1=flist[0][3]
    width_value2=flist[0][4]
    width_value3=flist[0][5]
    return render_template('result2.html', foodlist = flist, food_name = food_n, img_p = img_path, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)
###여기까지

###모델 기타
@app.route("/upload_done_gita", methods=["POST"])
def upload_done_gita():
    uploaded_files = request.files["file"]

    original_name = uploaded_files.filename

    # 현재 디렉토리와 상대 경로를 합쳐서 저장 경로를 만듭니다.
    save_path = os.path.join(upload_folder, original_name)
    print(save_path,"haha")
    if os.path.exists(save_path):
        print("delete file")
        os.remove(save_path)
    uploaded_files.save(save_path)

    return redirect(url_for("model_gita", filepath=save_path))

@app.route("/model_gita", methods=["GET", "POST"])
def model_gita():
    filepath = request.args.get('filepath', '')
    filepath = unquote(filepath)
    if os.path.exists(filepath):
        print(filepath, " exists!")
    else:
        print(filepath, " not exists!")
    #img_path = f"app/static/img/1.jpg"
    img_path = filepath
    result = modelgita.model_gita(filepath)
    print(result)
    global food
    food=result["TOP1"]
    food_n = food
    flist = food_list(food_n)
    print("flist:",flist)
    email=session.get("email")
    #email,now_t,food_name, foodlist
    add_food(food_n, flist ,email)
    width_value4=flist[0][1]
    width_value5=flist[0][2]
    width_value1=flist[0][3]
    width_value2=flist[0][4]
    width_value3=flist[0][5]
    return render_template('result2.html', foodlist = flist, food_name = food_n, img_p = img_path, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)
###여기까지

###모델 해산물
@app.route("/upload_done_haesanmul", methods=["POST"])
def upload_done_haesanmul():
    uploaded_files = request.files["file"]

    original_name = uploaded_files.filename

    # 현재 디렉토리와 상대 경로를 합쳐서 저장 경로를 만듭니다.
    save_path = os.path.join(upload_folder, original_name)
    print(save_path,"haha")
    if os.path.exists(save_path):
        print("delete file")
        os.remove(save_path)
    uploaded_files.save(save_path)

    return redirect(url_for("model_haesanmul", filepath=save_path))

@app.route("/model_haesanmul", methods=["GET", "POST"])
def model_haesanmul():
    filepath = request.args.get('filepath', '')
    filepath = unquote(filepath)
    if os.path.exists(filepath):
        print(filepath, " exists!")
    else:
        print(filepath, " not exists!")
    #img_path = f"app/static/img/1.jpg"
    img_path = filepath
    result = modelhaesanmul.model_haesanmul(filepath)
    print(result)
    global food
    food=result["TOP1"]
    food_n = food
    flist = food_list(food_n)
    print("flist:",flist)
    email=session.get("email")
    #email,now_t,food_name, foodlist
    add_food(food_n, flist ,email)
    width_value4=flist[0][1]
    width_value5=flist[0][2]
    width_value1=flist[0][3]
    width_value2=flist[0][4]
    width_value3=flist[0][5]
    return render_template('result2.html', foodlist = flist, food_name = food_n, img_p = img_path, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)
###여기까지

###모델 밀가루
@app.route("/upload_done_milgalu", methods=["POST"])
def upload_done_milgalu():
    uploaded_files = request.files["file"]

    original_name = uploaded_files.filename

    # 현재 디렉토리와 상대 경로를 합쳐서 저장 경로를 만듭니다.
    save_path = os.path.join(upload_folder, original_name)
    print(save_path,"haha")
    if os.path.exists(save_path):
        print("delete file")
        os.remove(save_path)
    uploaded_files.save(save_path)

    return redirect(url_for("model_milgalu", filepath=save_path))

@app.route("/model_milgalu", methods=["GET", "POST"])
def model_milgalu():
    filepath = request.args.get('filepath', '')
    filepath = unquote(filepath)
    if os.path.exists(filepath):
        print(filepath, " exists!")
    else:
        print(filepath, " not exists!")
    #img_path = f"app/static/img/1.jpg"
    img_path = filepath
    result = modelmilgalu.model_milgalu(filepath)
    print(result)
    global food
    food=result["TOP1"]
    food_n = food
    flist = food_list(food_n)
    print("flist:",flist)
    email=session.get("email")
    #email,now_t,food_name, foodlist
    add_food(food_n, flist ,email)
    width_value4=flist[0][1]
    width_value5=flist[0][2]
    width_value1=flist[0][3]
    width_value2=flist[0][4]
    width_value3=flist[0][5]
    return render_template('result2.html', foodlist = flist, food_name = food_n, img_p = img_path, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)
###여기까지

###모델 떡
@app.route("/upload_done_tteog", methods=["POST"])
def upload_done_tteog():
    uploaded_files = request.files["file"]

    original_name = uploaded_files.filename

    # 현재 디렉토리와 상대 경로를 합쳐서 저장 경로를 만듭니다.
    save_path = os.path.join(upload_folder, original_name)
    print(save_path,"haha")
    if os.path.exists(save_path):
        print("delete file")
        os.remove(save_path)
    uploaded_files.save(save_path)

    return redirect(url_for("model_tteog", filepath=save_path))

@app.route("/model_tteog", methods=["GET", "POST"])
def model_tteog():
    filepath = request.args.get('filepath', '')
    filepath = unquote(filepath)
    if os.path.exists(filepath):
        print(filepath, " exists!")
    else:
        print(filepath, " not exists!")
    #img_path = f"app/static/img/1.jpg"
    img_path = filepath
    result = modeltteog.model_tteog(filepath)
    print(result)
    global food
    food=result["TOP1"]
    food_n = food
    flist = food_list(food_n)
    print("flist:",flist)
    email=session.get("email")
    #email,now_t,food_name, foodlist
    add_food(food_n, flist ,email)
    width_value4=flist[0][1]
    width_value5=flist[0][2]
    width_value1=flist[0][3]
    width_value2=flist[0][4]
    width_value3=flist[0][5]
    return render_template('result2.html', foodlist = flist, food_name = food_n, img_p = img_path, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)
###여기까지

###모델 야채류
@app.route("/upload_done_yachaelyu", methods=["POST"])
def upload_done_yachaelyu():
    uploaded_files = request.files["file"]

    original_name = uploaded_files.filename

    # 현재 디렉토리와 상대 경로를 합쳐서 저장 경로를 만듭니다.
    save_path = os.path.join(upload_folder, original_name)
    print(save_path,"haha")
    if os.path.exists(save_path):
        print("delete file")
        os.remove(save_path)
    uploaded_files.save(save_path)

    return redirect(url_for("model_yachaelyu", filepath=save_path))

@app.route("/model_yachaelyu", methods=["GET", "POST"])
def model_yachaelyu():
    filepath = request.args.get('filepath', '')
    filepath = unquote(filepath)
    if os.path.exists(filepath):
        print(filepath, " exists!")
    else:
        print(filepath, " not exists!")
    #img_path = f"app/static/img/1.jpg"
    img_path = filepath
    result = modelyachaelyu.model_yachaelyu(filepath)
    print(result)
    global food
    food=result["TOP1"]
    food_n = food
    flist = food_list(food_n)
    print("flist:",flist)
    email=session.get("email")
    #email,now_t,food_name, foodlist
    ###
    add_food(food_n, flist ,email)
    ###
    width_value4=flist[0][1]
    width_value5=flist[0][2]
    width_value1=flist[0][3]
    width_value2=flist[0][4]
    width_value3=flist[0][5]

    return render_template('result2.html', foodlist = flist, food_name = food_n, img_p = img_path, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)
###여기까지

##음식이름 직접입력
@app.route('/search_f', methods=['GET', 'POST'])
def search_f():
    return render_template("search_f.html")

@app.route('/re_foodname',methods=['get','post'])
def re_foodname():
    if request.method == 'POST':
        re_foodname = request.form.get('re_foodname')
        food_n = re_foodname
        flist = food_list(food_n)
        print("flist:",flist)   #음식 db에서 조회하기
        email=session.get("email")  #이메일 세션
        #email,now_t,food_name, foodlist
        ###tb_personal 테이블에 데이터 추가
        add_food(food_n, flist ,email)
        ###
        width_value4=flist[0][1]
        width_value5=flist[0][2]
        width_value1=flist[0][3]
        width_value2=flist[0][4]
        width_value3=flist[0][5]
    return render_template('result2.html', foodlist = flist, food_name = food_n, width_value1=width_value1,width_value2=width_value2,width_value3=width_value3,width_value4=width_value4,width_value5=width_value5)

###음식이름 직접입력


#음식 섭취 시간 고르는 템플릿
@app.route('/selectmeal')
def selectmeal():
    #foodlist 그대로 받아오기
    #tb_personal에 방금 업로드 된 행을 가져온다.
    return render_template("selectmeal.html")

#음식 섭취 시간 고르는 템플릿에서 받은 값을 db로 전달
@app.route('/add_data', methods=['POST'])
def save_data():
    if request.method == 'POST':
        mealtime = request.form['mealtime']
        email=session.get("email")
        update_mealtime(email,mealtime)
    return redirect(url_for('mypage_html'))

@app.route('/mypage')
def mypage():
    return redirect(url_for('mypage_html'))


@app.route('/mypage_html', methods=['GET', 'POST'])
def mypage_html():
    email=session.get("email")
    standard_w_value=standard_w(email)
    calc_needk=calc_need_kcal(email)    #return return s1 ->s1 사용자의 최소 하루 필요 열량:했고
    record_li=get_recent_records(email) #return record_list:했고
    calc_t_k=calc_total_kcal(email)     #return total_kcal_records ->total :했고
    print("calc_t_k:",calc_t_k)
    compare_k=compare_kcal(calc_t_k,calc_needk)   #1일 권장 칼로리의 양은 #return s1,r
    todays_total_v=total_today(email)
    return render_template('mypage.html',todays_total_val=todays_total_v,record_list = record_li, calc_needk=calc_needk, calc_t_k=calc_t_k,compare_k=compare_k,standard_w_value=standard_w_value)

@app.route('/calc_on_mypage', methods=['GET', 'POST'])
def calc_on_mypage():
    email=session.get("email")
    standard_w_value=standard_w(email)
    calc_needk=calc_need_kcal(email)    #return return s1 ->s1 사용자의 최소 하루 필요 열량:했고
    record_li=get_recent_records(email) #return record_list:했고
    calc_t_k=calc_total_kcal(email)     #return total_kcal_records ->total :했고
    print("calc_t_k:",calc_t_k)
    compare_k=compare_kcal(calc_t_k,calc_needk)   #1일 권장 칼로리의 양은 #return s1,r
    cmp_on_mypage_val = None

    if request.method == 'POST':
        activity = request.form.get('activity_on_mypage')  #직접 mypage에서 고르기
        todays_total=total_today(email)     #오늘 kcal total
        print("오늘 토탈:",todays_total)
        todays_total_v = todays_total[0][0]
        print("오늘 토탈 튜플 뽑기:", todays_total)
        cmp_on_mypage_val=compare_on_mypage(activity, todays_total, email)
        print("cmp_on_mypage:",cmp_on_mypage_val)   #변수가 받은 건 리스트임(리스트 요소가 2개/양수 1개)
        if type(cmp_on_mypage_val) in (int, float):     #따라서 리스트로 받지 않은 애를 다시 str로 만들어서 넘긴다.
            cmp_on_mypage_val = int(cmp_on_mypage_val)
            cmp_on_mypage_val = [cmp_on_mypage_val]
            print("[cmp_on_mypage_val]:",cmp_on_mypage_val)
        else:   #이미 리스트로 받아온 애들은(s1,r) 이거나 (s1,todays_total_v)으로 넘어간다.
            pass
    return render_template('mypage.html', cmp_on_mypage_v=cmp_on_mypage_val, todays_total_val=todays_total_v,record_list = record_li, calc_needk=calc_needk, calc_t_k=calc_t_k,compare_k=compare_k,standard_w_value=standard_w_value)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

