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
from werkzeug.utils import secure_filename
import os
from datetime import datetime

db = Database()

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    cookie_val = request.cookies.get('userauth')
    if cookie_val != None and cookie_val != "":
        # Get list of users online from database
        online_users = list(db.get_users_online())
        users = []
        for user in online_users:
            users.append(user['username'])
        
        # Get list of images from static/uploaded
        photos = []
        for photo in db.get_photos():
            photos.append(photo)
        
        resp = render_template(url_for('index'), cookie=cookie_val, users=users, photos=photos)

    else:
        resp = redirect(url_for('login'))
    return resp

@app.route('/login', methods=["GET", "POST"])
def login():
    # Check if user is already logged in
    cookie = request.cookies.get('userauth')
    if cookie != None and cookie != "":
        return redirect('index')


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
                
                # Set user online
                db.update_user(user_data['username'], 
                    user_data['password'], 
                    salt=user_data['salt'], 
                    token=user_data['token'], 
                    listOfPets=user_data['listOfPets'],
                    logged_in=True
                )

                # Redirect to home page
                resp = make_response(redirect(url_for('index')))
                # Set authentication cookie
                resp.set_cookie('userauth', value=user_data['token'])
                return resp
            else:
                flash('Wrong password')
                return redirect(url_for('login'))


    return render_template("login.html",title='Sign In', form=form, logged_out=True)

@app.route("/register", methods=["GET", "POST"])
def register():
    # Check if user is already logged in
    cookie = request.cookies.get('userauth')
    if cookie != None and cookie != "":
        return redirect('index')

    
    form = RegistrationForm()

    if form.validate_on_submit():
        # Salt and hash password
        pw = form.password.data.encode('utf-8')
        salt = gensalt()
        hashed = hashpw(pw, salt)
        token = create_auth_token()

        db.update_user(form.username.data, hashed, salt=salt, token=token, listOfPets='')

        user_data = db.get_user(form.username.data)

        flash('You\'ve registered as {}. Go ahead and login!'.format(
            user_data['username']))
        return redirect(url_for('login'))
    
    return render_template("register.html", title='Register', form=form, logged_out=True)


@app.route("/profile", methods=["GET","POST"])
def user():
    cookie = request.cookies.get('userauth')

    if cookie != None and cookie != "":
        user_data = db.get_user_from_cookie(cookie)[0]
        resp = render_template("user.html", name=f"{user_data['username']}", listOfPets=f"{user_data['listOfPets']}")
    else:
        resp = redirect(url_for('login'))

    return resp

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

@app.route("/upload")
def upload_form():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)
    if file:
        if ".png" in file.filename or ".jpg" in file.filename:
            cookie = request.cookies.get('userauth')
            user_data = db.get_user_from_cookie(cookie)[0]
            username = user_data['username']

            filename = secure_filename(file.filename)
            path = os.path.join(os.path.dirname(__file__), f"static/uploaded/{filename}")
            file.save(path)

            uploadDate = datetime.today()

            db.update_photo(
                photo_path=f"static/uploaded/{filename}",
                username=username,
                upload_date=uploadDate
            )
            
            return redirect(url_for( 'index' ))