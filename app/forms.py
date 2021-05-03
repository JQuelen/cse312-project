from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Sign Up')   

class EditProfileForm(FlaskForm):
    listOfPets = StringField('List Of Pets')
    submit = SubmitField('Confirm') 

class UploadImageForm(FlaskForm):
    image = FileField('image')
    submit = SubmitField('Upload')