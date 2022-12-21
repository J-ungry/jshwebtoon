from typing import TYPE_CHECKING
from flask import Flask
import pymysql

#DB_USER="jsh"   #MySQL 계정명
DB_USER = "root" #정구리 MySQL 계정명
DB_NAME="jsh"   #MySQL DB명

def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"]="sdjisnoafsada"    #비밀키인데 의미 없음. 바꾸지 마세요.
    
    #Blueprint 등록 -> 이거 안되면 route에서 url 못 받아옴
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
    
    return app

# MySQL 연결 함수
def connect_db():
    db = pymysql.connect(   
        host="localhost",
        port=3306,
        user=DB_USER,
        #passwd="bread!123",
        passwd="duffufK123!",
        db=DB_NAME,
        charset="utf8"
        )
    print("connect MySQL")
    return db