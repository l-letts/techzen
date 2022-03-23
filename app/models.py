# from . import db
import unicodedata
from flask import Flask
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@localhost/dev_techzen_db"
app.config["MYSQL_DATABASE_HOST"] = "db"

db = SQLAlchemy(app)


class SignUpProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'studentssignup'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(255))
    password=db.Column(db.String(255))

    def __init__(self,first_name,last_name,username,email,password):
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.email=email
        self.password=generate_password_hash(password,method='pbkdf2:sha256')


class LoanApplication(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    sex = db.Column(db.String(80))
    phonenumber = db.Column(db.Integer)
    sid = db.Column(db.String(80))
    trn = db.Column(db.String(1000))
    address = db.Column(db.String(255))
    email = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    

    def __init__(self, first_name, last_name, sex, phonenumber, sid, trn, address,email, photo):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.phonenumber = phonenumber
        self.sid = sid
        self.trn = trn
        self.address = address
        self.email = email
        self.photo = photo

class University(db.Model):
    __tablename__ = 'university'
    sid = db.Column(db.String(80), primary_key=True)
    university_name = db.Column(db.Integer)
    student_major = db.Column(db.String(255))
    student_faculty = db.Column(db.String(255))
    student_tuition = db.Column(db.String(255))
    univeristy_contact = db.Column(db.Integer)
    

    def __init__(self, sid, university_name, student_major, student_faculty, student_tuition, university_contact):
        self.student_tuition = student_tuition
        self.university_name = university_name
        self.student_major = student_major
        self.student_faculty = student_faculty
        self.sid = sid
        self.university_contact = university_contact

class CreditScore(db.Model):
    __tablename__ = 'creditscore'
    sid = db.Column(db.String(80), primary_key=True)
    cscore = db.Column(db.Integer)

    def __init__(self, sid, cscore):
        self.sid = sid
        self.cscore = cscore
     
class Contract(db.Model):
    __tablename__ = 'contract'
    sid = db.Column(db.String(80), primary_key = True)
    student_name = db.Column(db.Integer)
    date = db.Column(db.DateTime())
    student_address = db.Column(db.String(255))
    student_dob = db.Column(db.Date())
    student_signature = db.Column(db.Integer)
    

    def __init__(self, sid, student_name, date, student_address, student_dob, student_signature):
        self.student_dob = student_dob
        self.student_name = student_name
        self.date = date
        self.student_address = student_address
        self.sid = sid
        self.student_signature = student_signature

class Loan(db.Model):
    __tablename__ = 'loan'
    loanid = db.Column(db.String(80), primary_key = True)
    loan_type = db.Column(db.Integer)
    loan_status = db.Column(db.String(255))

    def __init__(self, loanid, loan_type, date, loan_status):
            self.loan_type = loan_type
            self.date = date
            self.loan_status = loan_status


class LoanAdmin(db.Model):
    __tablename__ = 'loanadmin'

    loan_admin_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(255))
    password=db.Column(db.String(255))

    def __init__(self,first_name,last_name,username,email,password):
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.email=email
        self.password=generate_password_hash(password,method='pbkdf2:sha256')
    
class Gurantor(db.Model):
    __tablename__ = 'gurantor'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    gurantor_occupation = db.Column(db.String(80))
    gurantor_phonenumber = db.Column(db.Integer)
    gurantor_salary = db.Column(db.Float)
    gurantor_address = db.Column(db.String(255))
    loanid = db.Column(db.String(80))
    sid = db.Column(db.String(80), primary_key = True)
    

    def __init__(self, first_name, last_name, gurantor_occupation, gurantor_phonenumber, gurantor_salary,gurantor_address,loanid, sid):
        self.first_name = first_name
        self.last_name = last_name
        self.gurantor_occupation = gurantor_occupation
        self.gurantor_phonenumber = gurantor_phonenumber
        self.gurantor_salary = gurantor_salary
        self.gurantor_address = gurantor_address
        self.loanid = loanid
        self.sid = sid
        

class LoanPrioritization(db.Model):
    __tablename__ = 'loanprioritization'
    loanid = db.Column(db.String(80), primary_key = True)
    priority_id = db.Column(db.Integer)
   

    def __init__(self, loanid, priority_id):
            self.priority_id = priority_id
        
class Payment(db.Model):
    __tablename__ = 'payment'
    sid = db.Column(db.String(80), primary_key = True)
    loanid = db.Column(db.String(80), primary_key = True)
    payment_amount = db.Column(db.Integer)
    paymemt_date = db.Column(db.Date())
   

    def __init__(self, loanid, payment_amount, payment_date):
            self.payment_amount = payment_amount
            self.payment_date = payment_date



    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicodedata(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)