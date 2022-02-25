from . import db
from werkzeug.security import generate_password_hash

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
    __tablename__ = 'studentsloanapp'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phonenumber = db.Column(db.Integer(255))
    sid = db.Column(db.String(80))
    trn = db.Column(db.String(1000))
    address = db.Column(db.String(255))
    email = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    

    def __init__(self, first_name, last_name, phonenumber, sid, trn, address,email, photo):
        self.first_name = first_name
        self.last_name = last_name
        self.phonenumber = phonenumber
        self.sid = sid
        self.trn = trn
        self.address = address
        self.email = email
        self.photo = photo

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)