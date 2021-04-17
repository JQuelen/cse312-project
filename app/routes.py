from app import application
from flask import render_template

temp_db = {"user": "  "}

@application.route('/')
@application.route('/index')
def index():
    user = temp_db["user"]
    return render_template("test.html", temp_db=user)

@application.route('/login', methods=["GET", "POST"])
def login():
    #user = temp_db["user"]
    #temp_db["user"] = methods["POST"].username
    return render_template("login.html")

@application.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")
