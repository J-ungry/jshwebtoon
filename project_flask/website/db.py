import pymysql

DB_USER="jsh"   #MySQL 계정명
#DB_USER = "root" #정구리 MySQL 계정명
DB_NAME="jsh"   #MySQL DB명

# MySQL 연결 함수
def connect_db():
    db = pymysql.connect(   
        host="localhost",
        port=3306,
        user=DB_USER,
        passwd="bread!123",
        #passwd="duffufK123!",
        db=DB_NAME,
        charset="utf8"
        )
    print("connect MySQL")
    return db

# cursor 생성 함수
def create_cursor():
    db=connect_db()
    cursor=db.cursor()
    print("create cursor")
    return cursor

# db.commit()
def db_commit():
    db=connect_db()
    db.commit()
    print("commit")
        
def jungry_query(query):
    cursor=create_cursor()
    cursor.execute(query)
    datas = cursor.fetchall()
    return datas
    