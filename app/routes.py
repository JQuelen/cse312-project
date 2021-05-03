from app import app
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import make_response
from flask import request
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.forms import EditProfileForm
from app.forms import UploadImageForm
from app.database import Database
from bcrypt import gensalt, hashpw
from app.authentication import create_auth_token

db = Database()

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    cookie_val = request.cookies.get('userauth')
    return render_template(url_for('index'), cookie = cookie_val)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user_data = db.get_user(form.username.data)

        if user_data == None:
            flash('User {} does not exist.'.format(
                form.username.data))
            return redirect(url_for('login'))
        else:
            hashed_stored = user_data['password']
            salt_stored = user_data['salt']
            hashed_input = hashpw(form.password.data.encode('utf-8'), salt_stored)

            if hashed_input == hashed_stored:
                flash('Hi, {}'.format(
                    user_data['username']))
                # Redirect to home page
                resp = make_response(redirect(url_for('index')))
                # Set authentication cookie
                resp.set_cookie('userauth', value=user_data['token'])
                return resp
            else:
                flash('Wrong password')
                return redirect(url_for('login'))


    return render_template("login.html",title='Sign In', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Salt and hash password
        pw = form.password.data.encode('utf-8')
        salt = gensalt()
        hashed = hashpw(pw, salt)
        token = create_auth_token()

        db.update_user(form.username.data, hashed, salt=salt, token=token)

        user_data = db.get_user(form.username.data)

        flash('Registration requested for user {}'.format(
            user_data['username']))
        return redirect(url_for('login'))
    
    return render_template("register.html", title='Register', form=form)


@app.route("/profile", methods=["GET","POST"])
def user():
    cookie = request.cookies.get('userauth')
    user_data = db.get_user_from_cookie(cookie)[0]

    return render_template("user.html", name=f"{user_data['username']}", listOfPets=f"{user_data['listOfPets']}")

@app.route("/editProfile", methods=["GET","POST"])
def editProfile():
    cookie = request.cookies.get('userauth')
    user_data = db.get_user_from_cookie(cookie)[0]
    form = EditProfileForm()
    if form.validate_on_submit():
        user_data['listOfPets'] = form.listOfPets.data

        db.update_user(username=user_data['username'], 
            password=user_data['password'], 
            salt=user_data['salt'], 
            token=user_data['token'], 
            listOfPets=user_data['listOfPets'])
        
        return redirect(url_for('user'))

    return render_template("editProfile.html", form=form)

@app.route("/upload", methods=["GET","POST"])
def upload():
    form = UploadImageForm()
    return render_template("upload.html")     