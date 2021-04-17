from app import application
from flask import render_template

@application.route('/')
@application.route('/index')
def index():
    return "Hello, World"
    user = "Test User"
    return render_template("base.html", name=user)
