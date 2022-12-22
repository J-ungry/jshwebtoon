from flask import Blueprint,render_template,session
from website import db,models

cursor=db.create_cursor()
views = Blueprint("views",__name__)

@views.route("/")
def index():
    a=models.main()
    print(a)
    return render_template("index.html",a=a)

@views.route("/introduce_service")
def introduce_service():
    return render_template("introduce_service.html")

@views.route("/introduce_team")
def introduce_team():
    return render_template("introduce_team.html")

@views.route("/input_keyword")
def input_keyword():
    if session:
        return_genre=[]
        #장르 = 1 소재 = 2 분위기 = 3 수상작 = 4 등장인물관계 = 5 원작웹툰 =6 
        for type in range(1,7):
            cursor.execute(f"""
                SELECT DISTINCT keyword FROM keyword WHERE type='{type}' ORDER BY keyword
            """)
            if type==1:
                genre=cursor.fetchall()
            elif type==2:
                sojae=cursor.fetchall()
            elif type==3:
                atm=cursor.fetchall()
            elif type==4:
                soosang=cursor.fetchall()
            elif type==5:
                rel=cursor.fetchall()
            else:
                origin_webtoon=cursor.fetchall()
        
        for i in range(len(genre)):
            return_genre.append(genre[i][0])
        
        result,dsModel=models.main()
        print(result)
        print(dsModel)
        
        return render_template("input_keyword.html",genre=return_genre)
    