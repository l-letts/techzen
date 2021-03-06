from . import db
import datetime
import unicodedata
from werkzeug.security import generate_password_hash


class SignUpProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'studentssignup'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    sid = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(255))
    password=db.Column(db.String(255))

    def __init__(self,first_name,last_name,sid,username,email,password):
        self.first_name=first_name
        self.last_name=last_name
        self.sid = sid
        self.username=username
        self.email=email
        self.password=generate_password_hash(password,method='pbkdf2:sha256')


class LoanApplication(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    sex = db.Column(db.String(80))
    phonenumber = db.Column(db.Integer)
    sid = db.Column(db.String(80))
    trn = db.Column(db.String(1000))
    address = db.Column(db.String(255))
    email = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    status = db.Column(db.String(255))
    

    def __init__(self, first_name, last_name, sex, phonenumber, sid, trn, address,email, photo, status):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.phonenumber = phonenumber
        self.sid = sid
        self.trn = trn
        self.address = address
        self.email = email
        self.photo = photo
        self.status = status

class University(db.Model):
    __tablename__ = 'university'
    sid = db.Column(db.String(80), primary_key=True)
    university_name = db.Column(db.String(255))
    student_major = db.Column(db.String(255))
    student_faculty = db.Column(db.String(255))
    student_tuition = db.Column(db.String(255))

    

    def __init__(self, sid, university_name, student_major, student_faculty, student_tuition):
        self.student_tuition = student_tuition
        self.university_name = university_name
        self.student_major = student_major
        self.student_faculty = student_faculty
        self.sid = sid


class CreditScore(db.Model):
    __tablename__ = 'creditscore'
    sid = db.Column(db.String(80), primary_key=True)
    cscore = db.Column(db.Integer)

    def __init__(self, sid, cscore):
        self.sid = sid
        self.cscore = cscore
        
class AdminLog(db.Model):
    __tablename__ = 'adminlog'
    logid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    logdata = db.Column(db.Text)
    time = db.Column(db.DateTime)

    def __init__(self, logdata, time):

        self.logdata = logdata
        self.time = time
     
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
    loanid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    loan_type = db.Column(db.String(255))
    loan_status = db.Column(db.String(255))
    sid = db.Column(db.Integer)
    length = db.Column(db.Integer)
    interestrate = db.Column(db.Integer)
    loanamount = db.Column(db.Integer)
    start_date = db.Column(db.String(80))
    moratorium = db.Column(db.String(255))

    def __init__(self, loan_type, loan_status, sid, length, interestrate, loanamount, start_date, moratorium):
        self.loan_type = loan_type
        self.loan_status = loan_status
        self.sid = sid
        self.length = length
        self.interestrate = interestrate
        self.loanamount = loanamount
        self.start_date = start_date
        self.moratorium = moratorium


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
    
class Guarantor(db.Model):
    __tablename__ = 'guarantor'
    #id does not auto increment.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    guarantor_occupation = db.Column(db.String(80))
    guarantor_phonenumber = db.Column(db.Integer)
    guarantor_salary = db.Column(db.Float)
    guarantor_address = db.Column(db.String(255))
    # loanid = db.Column(db.String(80))
    sid = db.Column(db.String(80))
    

    def __init__(self, first_name, last_name, guarantor_occupation, guarantor_phonenumber, guarantor_salary,guarantor_address, sid):
        self.first_name = first_name
        self.last_name = last_name
        self.guarantor_occupation = guarantor_occupation
        self.guarantor_phonenumber = guarantor_phonenumber
        self.guarantor_salary = guarantor_salary
        self.guarantor_address = guarantor_address

        self.sid = sid
        

class LoanPrioritization(db.Model):
    __tablename__ = 'loanprioritization'
    loanid = db.Column(db.String(80), primary_key = True)
    priority_id = db.Column(db.Integer)
    interest = db.Column(db.Numeric(10,2))
   

    def __init__(self, loanid, priority_id, interest):
        self.loanid = loanid
        self.priority_id = priority_id
        self.interest = interest
            
            
class GraphicalAnalytics(db.Model):
    __tablename__ = 'graphicalanalytics'
    loanid = db.Column(db.String(80), primary_key = True)
    loanamount = db.Column(db.Integer)
    interestrate = db.Column(db.Integer)
    sid = db.Column(db.Integer)
   

    def __init__(self, loanid, loanamount, interestrate, sid):
        self.loanid = loanid
        self.loanamount = loanamount
        self.interestrate = interestrate
        self.sid = sid
        
class Payment(db.Model):
    __tablename__ = 'payment'
    sid = db.Column(db.String(80))
    loanid = db.Column(db.String(80))
    payment_amount = db.Column(db.Integer)
    payment_date = db.Column(db.String(80))
    paymentid = db.Column(db.Integer, primary_key = True, autoincrement = True)
   

    def __init__(self, sid, loanid, payment_amount, payment_date):
        self.sid = sid
        self.loanid = loanid
        self.payment_amount = payment_amount
        self.payment_date = payment_date

        
class Img(db.Model):
    __tablename__ = 'image'
    sid = db.Column(db.String(80))
    imageid = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=True)
    
    def __init__(self, sid, img, name, mimetype):
        self.sid = sid
        self.img = img
        self.name = name
        self.mimetype = mimetype



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