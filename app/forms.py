from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms.widgets import TextArea
from wtforms import StringField, PasswordField, TextAreaField,SelectField, IntegerField, DateField
from wtforms.validators import InputRequired, DataRequired, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed


class SignUpForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()] ,description="Please enter your first name." )
    lname = StringField('Last Name', validators =[InputRequired()],description="Please enter your last name.")
    sid = StringField('Student ID', validators =[InputRequired()],description="Please enter your Student ID.")
    username = StringField('Username', validators=[InputRequired()],description="Please enter a username.")
    email = StringField('Email', validators=[DataRequired(), Email()], description='Please enter your email address.')
    password = PasswordField('Password', validators=[InputRequired()])



class LoanApplicationForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    lname = StringField('Last Name', validators=[InputRequired()])
    sex = StringField('Sex', validators=[InputRequired()])
    phone = StringField('Phone Number', validators=[InputRequired()])
    sid = StringField('Student ID', validators=[InputRequired()])
    trn = StringField('Student TRN', validators=[InputRequired()]) 
    address = StringField('Address', validators=[InputRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()], description='Please enter your email address.')
    photo = FileField('Photo',validators=[FileRequired(), FileAllowed(['jpg','png'], 'Please Upload Your Image Only!')])
    selfie = FileField('Selfie',validators=[FileRequired(), FileAllowed(['jpg','png'], 'Please Upload Your Selfie Only!')])
   
class GuarantorForm(FlaskForm):
    gfname = StringField('First Name', validators=[InputRequired()])
    glname = StringField('Last Name', validators=[InputRequired()])
    goccupation = StringField('Occupation', validators=[InputRequired()])
    gphone = StringField('Phone Number', validators=[InputRequired()])
    gsalary = StringField('Guarantor Salary', validators=[InputRequired()])
    gaddress = StringField('Address', validators=[InputRequired()])
    loanid = StringField('Loan ID', validators=[InputRequired()])
    sid = StringField('Student ID', validators=[InputRequired()])
        
    
class LoanForm(FlaskForm):
    loan_status = StringField('Loan Status', validators=[InputRequired()])
    sid = StringField('Student ID', validators=[InputRequired()])
    length = StringField('Length in Months', validators=[InputRequired()])
    interestrate = IntegerField('Interest Rate', validators=[InputRequired()])
    loanamount = IntegerField('Loan Amount', validators=[InputRequired()])
    
    
class LoanAnalyticsPrioritizerForm(FlaskForm):
    loanid = StringField('Loan ID', validators=[InputRequired()])
    priorityid = StringField('Priority ID', validators=[InputRequired()])
    interest = IntegerField('Interest', validators=[InputRequired()])
    
class PaymentForm(FlaskForm):
    sid = StringField('Student ID', validators=[InputRequired()])
    loanid = StringField('Loan ID', validators=[InputRequired()])
    paymentamount = StringField('Payment Amount', validators=[InputRequired()])
    paymentdate = StringField('Date', validators=[InputRequired()])
