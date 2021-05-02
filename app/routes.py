from app import app
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.database import Database

dbobj = Database()
db = dbobj.db()

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template("index.html", name="ted")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))


    return render_template("login.html",title='Sign In', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    return render_template("register.html", title='Register', form=form)
