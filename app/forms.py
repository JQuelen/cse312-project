from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Sign Up')   

class EditProfileForm(FlaskForm):
    listOfPets = TextAreaField('Pets')
    submit = SubmitField('Save')

class UploadImageForm(FlaskForm):
    image = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    #submit = SubmitField('Upload')

class MessageForm(FlaskForm):
    message = TextAreaField('message', validators=[
        DataRequired()])
    submit = SubmitField('Submit')

class ReplyForm(FlaskForm):
    message = TextAreaField('message', validators=[
        DataRequired()])
    submit = SubmitField('Reply')