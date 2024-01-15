from flask import Flask, render_template, request, redirect, url_for
import sys
import pymysql
from tensorflow.python.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
from matplotlib import font_manager,rc
#폰트 경로
#font_path = r'C:\\Windows\\Fonts\\Arial\\fariblk'
#폰트 이름 얻어오기
#font_name = font_manager.FontProperties(fname=font_path).get_name()
#font 설정
#plt.rc('font',family=font_name)

def mk_graph(flist):
    #가지고 들어와야 되는 요소: model_gogilyu.list의 list[0][1]~ list[0][5]
    # 음식 이름과 각각의 값을 추출
    calories = [food[2] for food in flist]
    tan = [food[3] for food in flist]
    dan = [food[4] for food in flist]
    gee = [food[5] for food in flist]

    # 그래프 그리기
    plt.figure(figsize=(10, 6))  # 그래프 크기 설정

    bar_width = 0.2  # 막대의 너비 설정
    index = range(len(flist))

    plt.bar(index, calories, bar_width, label='Calories', color='r', alpha=0.7)
    plt.bar([i + bar_width for i in index], tan, bar_width, label='Tan', color='g', alpha=0.7)
    plt.bar([i + 2 * bar_width for i in index], dan, bar_width, label='Dan', color='b', alpha=0.7)
    plt.bar([i + 3 * bar_width for i in index], gee, bar_width, label='Gee', color='y', alpha=0.7)

    plt.xlabel('Foods')
    plt.ylabel('Values')
    plt.title('Food Nutrition Information')
    plt.xticks([i + 1.5 * bar_width for i in index], flist)  # x 축 레이블 설정
    plt.legend()

    plt.tight_layout()

    # 그래프를 이미지로 변환
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # 이미지를 Base64로 인코딩
    image_base64 = base64.b64encode(buffer.read()).decode()


    # 그래프 창 닫기
    plt.close()

    return image_base64