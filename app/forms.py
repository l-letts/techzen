from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms.widgets import TextArea
from wtforms import StringField, PasswordField, TextAreaField,SelectField
from wtforms.validators import InputRequired, DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed


class SignUpForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()] ,description="Please enter your first name." )
    lname = StringField('Last Name', validators =[InputRequired()],description="Please enter your last name.")
    username = StringField('Username', validators=[InputRequired()],description="Please enter a username.")
    email = StringField('Email', validators=[DataRequired(), Email()], description='Please enter your email address.')
    password = PasswordField('Password', validators=[InputRequired()])



class LoanApplicationForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    lname = StringField('Last Name', validators=[InputRequired()])
    phone = StringField('Phone Number', validators=[InputRequired()])
    trn = StringField('Student TRN', validators=[InputRequired()]) 
    address = StringField('Address', validators=[InputRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()], description='Please enter your email address.')
    photo = FileField('Photo',validators=[FileRequired(), FileAllowed(['jpg','png'], 'Please Upload Your Image Only!')])
   
class GuarantorForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    lname = StringField('Last Name', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    phone = StringField('Phone Number', validators=[InputRequired()])