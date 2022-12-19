from flask import Blueprint,render_template,session

views = Blueprint("views",__name__)

@views.route("/")
def index():
    return render_template("index.html")

@views.route("/introduce_service")
def introduce_service():
    return render_template("introduce_service.html")

@views.route("/introduce_team")
def introduce_team():
    return render_template("introduce_team.html")

@views.route("/input_keyword")
def input_keyword():
    return render_template("input_keyword.html")
    
    