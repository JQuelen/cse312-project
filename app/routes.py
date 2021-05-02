from app import app
from flask import render_template
from app.forms import LoginForm
from app.forms import RegistrationForm

temp_db = {"user": "  "}

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    user = temp_db["user"]
    return render_template("index.html", name="ted")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    #user = temp_db["user"]
    #temp_db["user"] = methods["POST"].username
    return render_template("login.html",form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    return render_template("register.html",form=form)
