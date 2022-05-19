"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from audioop import avg
import os
from tabnanny import check
from app import app, db
from app.models import Guarantor, University ,SignUpProfile, GraphicalAnalytics, LoanPrioritization, LoanApplication, Payment, Loan, AdminLog
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory, Response
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.forms import *
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import uuid as uuid
import math
from datetime import datetime
from sqlalchemy import desc, asc



# ##
# Routing for your application.
# ##

mysql = MySQL(app)


@app.route('/home')
def home():
    """Render website's home page."""
    return render_template('home.html')



# 
# The Application Route displays the various application forms:
# Student Information, Guarantor Information and University Information
# So that the applicant may apply for a loan through the system.
# 


@app.route('/application')
def application():
    """Render website's home page."""
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('application.html')



@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="TechZen")



# 
# On the Payment route, the applicant is able to make a payment
# for a loan in which they have taken. This directs the user to a
# form where the user inputs values for their Loan ID, Student ID,
# The amount they want to pay, as well as the current date.
#  

@app.route('/payment', methods=['POST', 'GET'])
def payment():
    """Render the website's payment."""
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))
    
    
    paymentform =PaymentForm()
    # Validate file upload on submit
    if request.method == 'POST' and paymentform.validate_on_submit():
        
        payment = Payment( 
            sid = paymentform.sid.data,
            loanid = paymentform.loanid.data,
            payment_amount= paymentform.paymentamount.data,
            payment_date= paymentform.paymentdate.data,

        )
        
        db.session.add(payment)

        db.session.commit()

        flash('Payment successful!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('payment.html', form=paymentform)

# This function is used to find the average of a list.
def average(lst):
    return sum(lst) / len(lst)

# This function calculates loan premium based on the formula:
# [P x R x (1+R)^N] / [(1+R)^N-1]
# The value is stored in the variable calc, and returned.
def premium(loanamount, interestrate, length):

    calc=(loanamount*interestrate/12*(pow(1+interestrate/12,length)))/(pow(1+interestrate/12,length)-1)
    return(calc)

# This function assists the dashboard by collecting the payment history of a particular
# loan, specified by passing in a Loan ID as its paramater. The Payment History
# is collected from the database and then appended to a list.
# Given that the list is empty, this means that there have been no payments made on the
# loan. In this case, the payment list is set at Zero (0).
# The final list is returned to the dashboard so that it may be used.
def getpaymenthistory(loanid):
    
    paymentlist = []
    foundvalue = Payment.query.filter(Payment.loanid==loanid).all()

    for x in foundvalue:
        if x.sid == session['sid']:
            paymentlist.append(x.payment_amount)

        
    if paymentlist==[]:

        paymentlist = [0]
        interestrate = 1
    
    return (paymentlist)


# On the getLoan route, the user's loans are all gathered from the database
# and are displayed to the front end in a table form, so that the user may
# see information on all their active loans.
# Should the user need to see his/her loans in their dashboard, in graphical
# format, they may click "View in Dashboard", in order to pass the loan id
# to the dashboard and display the loan.
@app.route('/getloan', methods=['POST', 'GET'])
def getLoan():
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))
    
    loanquery = Loan.query.filter(Loan.sid == session['sid']).all()

    
    if request.method == 'POST' :

        
        raw = request.form['submit']
        loanid, status = raw.split("_")
        
        if status == 'View':
            flash(f"Loanid extracted was: {loanid}", 'success')
            

    
    return render_template('getLoan.html', loans=loanquery, username = session['username'])


# The dashboard is the section that speaks to the requirement of the Graphical Analytics.
# On the Dashboard, the user is able to see information on their loans.
# The user is able to see information on their Payment History, Their Projected Loan Payback time, and
# The Interest that would be accrued alongside their payback.
# The route begins by grabbing the SID of the logged in user, and checks the database for any loan
# That the user has by filtering the database using their SID.
# Once the query is finished, if the user has any loans, the system displays them in a list format, which the
# user is able to navigate by clicking, to see their different loans.
# If the user does not have any loans, they may add a loan using the "Add Loan" button.
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))

    # Initializes the list of months.
    monthdictionary = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    currentsid = '12345'
    
    # Initializes variables. These variables will be overwritten in the case
    # that the user has loans active.
    loanid = 1
    start_number = 0
    paymentlist = [0]

    # The query checks the database for loans belonging to the SID of the logged in user.
    loanlst = Loan.query.filter(Loan.sid == session['sid']).all()


    # The request method accepts the loan id from the buttons on the page.
    # This is where user will navigate their various loans.
    if request.method == 'POST':
        loanid = request.form['submit']

        paymentlist = getpaymenthistory(loanid)
    # grabs the payment data
    
    # This query grabs the payment information of the user's loan.
    foundvalue = Payment.query.filter(Payment.loanid == loanid).all()
    loanquery = Loan.query.all()
    loandetails = [0]

    
    # The for loop checks the loan and initializes key variables.
    loanid = int(loanid)
    for x in loanquery:


        if x.loanid == loanid:
            loandetails = x
            loanid = x.loanid
            overallloan = x.loanamount
            interestrate = x.interestrate
            length = x.length
            start_date = x.start_date
            loanstat = "Yes"

            i = 0
            for c in monthdictionary:
                if start_date == c:
                    start_number = i
                i+=1

    if loanquery==[]:

        loandetails = []
        overallloan = 0
        interestrate = 1
        
    if loanid == 1:
        loanstat = "No"



    # In the case that there are no loans, the information of the user is passed through
    # this if statement to prevent calculation errors.
    if loandetails == [0]:
        overallloan = 0
        loanpay = [0]
        days = [1,2,3]
        interestprojection = [0]
        return render_template('dashboard.html',usrname=session['username'],
                                                paymentval=foundvalue, 
                                                paymentlst=json.dumps(paymentlist), 
                                                overall=json.dumps(overallloan), 
                                                loanpay=json.dumps(loanpay),
                                                paydays = json.dumps([0]), 
                                                days=json.dumps(days), 
                                                interest=json.dumps(interestprojection),
                                                loanstat = loanstat)
        

   
    # If there are loans active for the user, the if statement is ignored, and the program
    # continues as planned.
    
    loanpay = []
    loandata = []
    days = []
    i = start_number
    
    # the interest rate is initialized as a decimal, to account for percentages.
    interestrate = interestrate / 100
    
    # The premium is calculated by running the premium function and passing in the loan principal, interest rate
    # and the length of the loan.
    avgpay = premium(overallloan, interestrate, length)
    loanpremium = avgpay * length

    interest = 0
    interestprojection = []
    interestpayback = 0
    
    temploanpremium = overallloan
    
    
    # The values used in the graphs are calculated here.
    # This calculates the interest accrued as well as the
    # loan projection.
    days.append(str(monthdictionary[(i % 12)]))
    loanpay.append(temploanpremium)
    loandata.append(temploanpremium)
    for value in foundvalue:
        i += 1

        temploanpremium = temploanpremium - value.payment_amount
        loanpay.append(temploanpremium)
        loandata.append(temploanpremium)

        days.append(str(monthdictionary[(i % 12)]))
        
    # This calculates the projected time period expected to pay back the loan.
    while (temploanpremium-avgpay) >= 0:
        i += 1
        interestpayback = temploanpremium * (interestrate/12)
        principalamt = avgpay - interestpayback
        loanpay.append(temploanpremium-principalamt)
        loandata.append(temploanpremium)
            
        days.append(str(monthdictionary[(i % 12)]))
        temploanpremium = temploanpremium-principalamt
        interestprojection.append(interestpayback) 
        

    
    # This section initializes key information as session variables, so
    # that the system may use the variable in other sections of the program.
    session['loandata'] = loanpay
    session['daydata'] = days
    session['interestdata'] = interestprojection
    session['loanid'] = loanid
    session['premiumpay'] = avgpay
    if (temploanpremium-avgpay) < 0:
        temploanpremium = temploanpremium - temploanpremium
        loanpay.append(0)
        days.append(str(monthdictionary[((i+1) % 12)]))     

        


    paydays = []
    i = start_number
    for x in paymentlist:
        paydays.append(str(monthdictionary[((i+1) % 12)])) 
        i+=1
    upperpay = max(paymentlist)
    
    
    return render_template('dashboard.html', sid = session['sid'], loanid = loanid, loanamount = overallloan, loanstat = loanstat, loanlist = loanlst, maxpay=upperpay, paydays = json.dumps(paydays) , usrname=session['username'],paymentval=foundvalue, paymentlst=json.dumps(paymentlist), overall=json.dumps(overallloan), loanpay=json.dumps(loanpay), days=json.dumps(days), interest=json.dumps(interestprojection))
    
    # The schedule takes in the loan id of the loan selected and displays to the front end
    # the schedule that the applicant has to pay back the loan if they follow the loan premium,
    # and pay that amount monthly.
@app.route('/schedule', methods=['POST', 'GET'])
def schedule():
    
    # Instantiate your form class
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))

    
    infolst = []
    loandata = session['loandata']
    daydata = session['daydata']
    interestdata = session['interestdata']
    loanid = session['loanid']
    premiumpay = "${:,.2f}".format(session['premiumpay'])
    

    c = 0

    x = 0
    intcount = len(session['interestdata'])

    for loan in loandata:
        templst = []
        templst.append(c+1)
        templst.append(daydata[c])
        templst.append("${:,.2f}".format(loan))
        if x < (intcount-1):
            idata =interestdata[x]
            templst.append("${:,.2f}".format(idata))
        elif x == intcount-1:
            idata =interestdata[x]
            templst.append("${:,.2f}".format(idata))
            x+=1
        else:
            templst.append("${:,.2f}".format(0))
        infolst.append(templst)
        
        
        c+=1
        if x < (intcount-1):
            x += 1

    
    
    return render_template('schedule.html', premiumpay = premiumpay, loanid = loanid, infolst = infolst, loandata = session['loandata'], daydata = session['daydata'], interestdata = session['interestdata'])

    
    # This section uses similar code to that of the dashboard.
    # The difference here, however, is that the priority calculates the same information
    # in order to grab the loan out of a list that is calculated to select the loan
    # with the highest priority.
@app.route('/priority', methods=['POST', 'GET'])
def priority():
    
    # Instantiate your form class
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))


    loanid = 3
    start_number = 0
    paymentlist = [0]

    
    loanlst = Loan.query.filter(Loan.sid == session['sid']).all()
    loanquery = Loan.query.all()
    loandetails = [0]

    
    loantotallst = []
    for x in loanquery:

        if x.sid == int(session['sid']):

            loandetails = []
            loanid = x.loanid
            overallloan = x.loanamount
            interestrate = x.interestrate
            length = x.length
            
            loandetails.append(loanid)
            loandetails.append(overallloan)
            loandetails.append(interestrate)
            loandetails.append(length)

            loantotallst.append(loandetails)

    if loanquery==[]:

        loandetails = []
        overallloan = 0
        interestrate = 1




   
    interestrate = 6
    overallloan = 100
    length = 60
    
    
    interestlst = []
    
    
    
    o = 0
    
    for x in loantotallst:
        loaninterests = []
        overallloan = loantotallst[o][1]
        interestrate = loantotallst[o][2]
        length = loantotallst[o][3]
        
        # 
        loanpay = []
        i = start_number
        interestrate = interestrate / 100
        avgpay = premium(overallloan, interestrate, length)
        loanpremium = avgpay * length

        interest = 0
        interestprojection = []
        interestpayback = 0
        temploanpremium = overallloan
        
        loanpay.append(temploanpremium)
        # This calculates the projected time period expected to pay back the loan.

        
        
        
        

        while (temploanpremium-avgpay) >= 0:
            i += 1
            interestpayback = temploanpremium * (interestrate/12)
            principalamt = avgpay - interestpayback
            loanpay.append(temploanpremium-principalamt)
                

            temploanpremium = temploanpremium-principalamt
            interestprojection.append(interestpayback) 
            
            
        if (temploanpremium-avgpay) < 0:
                temploanpremium = temploanpremium - temploanpremium
                loanpay.append(0)
        
        loaninterests.append(loantotallst[o][0])
        loaninterests.append(sum(interestprojection))
        interestlst.append(loaninterests)


        o+=1

    
    prioritylst = []
    for x in interestlst:
        prioritylst.append(x[1])


    loaninfo = []
    higherprioritylst = []
    if prioritylst != []:
        higherpriority = max(prioritylst)

        higherprioritylst = []
        for x in interestlst:
            if higherpriority in x:
                higherprioritylst.append(x[0])
                higherprioritylst.append(x[1])
                
        loaninfo = []
        
        for x in loantotallst:
            
            if higherprioritylst[0] in x:
                
                overallloan = x[1]
                interestrate = x[2]
                length = x[3]
                loaninfo.append(higherprioritylst[0]) #loanid
                loaninfo.append("${:,.2f}".format(overallloan))
                loaninfo.append(interestrate)
                loaninfo.append(length)
                loaninfo.append("${:,.2f}".format(higherprioritylst[1])) #loaninterest
    
    return render_template('priority.html', loaninfo = loaninfo,prioritylst = higherprioritylst, loanlist = loanlst , usrname=session['username'])
    

# The register route is pretty much self explanatory. This is the standard
# sign up page for our user.
@app.route('/register', methods=['POST', 'GET'])
def register():

    # Instantiate your form class
    registerform=SignUpForm()
    # Validate file upload on submit
    if request.method == 'POST' and registerform.validate_on_submit():
 
        
        signup = SignUpProfile( 
            first_name = registerform.fname.data,
            last_name = registerform.lname.data,
            sid = registerform.sid.data,
            username = registerform.username.data,
            email = registerform.email.data,
            password = registerform.password.data
        )
        
        db.session.add(signup)
        print(signup)
        db.session.commit()

        flash('Registration Successful! Please Login below.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=registerform)

# In the loan application route, the user is required to submit information
# for their application profile in order to receive a loan.
# In this route, the user is also asked to upload two photos, of which will be
# checked alongside each other for their similarity status.
# This is done using the Face Verification API by PresentID.
@app.route('/apply', methods=['POST', 'GET'])
def loanApplication():
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))
    
    # Instantiate your form class
    applicationform=LoanApplicationForm()
    # Validate file upload on submit
    if request.method == 'POST' :
        
        # Get file data and save to your uploads folder
        
        photo = applicationform.photo.data
        photo2 = applicationform.selfie.data
        sid = applicationform.sid.data
        root_dir = os.getcwd()

        filename = str(sid) + "_A_" + secure_filename(photo.filename)
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        print(filename)
        
        filename2 = str(sid) + "_B_" + secure_filename(photo2.filename)
        photo2.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename2
        ))
        
        loanapplication = LoanApplication( 
            first_name = applicationform.fname.data,
            last_name = applicationform.lname.data,
            sex = applicationform.sex.data,
            phonenumber= applicationform.phone.data,
            sid = applicationform.sid.data,
            trn = applicationform.trn.data,
            address = applicationform.address.data,
            email = applicationform.email.data,
            photo= filename,
            status= "Waiting"

        )
        
        
        # API Call
        
        
        api_url = 'https://face-verification2.p.rapidapi.com/FaceVerification'
        api_key = '198bff86e4msh4cfe80801440c7ep1c1779jsn9a870a2e8dbe'
        
        root_dir = os.getcwd()
        image1_path =  os.path.join(root_dir, './uploads/')
        image1_name = filename
        image2_path = os.path.join(root_dir, './uploads/')
        image2_name = filename2

        files = {'Photo1': (image1_name, open(image1_path + image1_name, 'rb'), 'multipart/form-data'), 
                'Photo2': (image2_name, open(image2_path + image2_name, 'rb'), 'multipart/form-data')}
        header = {
            "x-rapidapi-host": "face-verification2.p.rapidapi.com",
            "x-rapidapi-key": api_key
        }
        response = requests.post(api_url, files=files, headers=header)
        print(response.text)
                
        if "The two faces belong to the same person." in response.text:        
            db.session.add(loanapplication)
            db.session.commit()
            flash('Student Information saved!', 'success')
            return redirect(url_for('application'))
        
        else:
            flash("The faces do not match!", 'danger')
            return redirect(url_for('loanApplication'))
        
        
        

    return render_template('loanapplication.html', form=applicationform)


    
# The guarantorForm route is where the user will input information relating to their guarantor. 
@app.route('/guarantor', methods=['POST', 'GET'])
def guarantorForm():
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))

    # Instantiate your form class
    guarantorform= GuarantorForm()
    # Validate file upload on submit
    if request.method == 'POST' and guarantorform.validate_on_submit():
        guarantor = Guarantor( 
            first_name = guarantorform.gfname.data,
            last_name = guarantorform.glname.data,
            guarantor_occupation = guarantorform.goccupation.data, 
            guarantor_phonenumber = guarantorform.gphone.data,
            guarantor_salary = guarantorform.gsalary.data,
            guarantor_address = guarantorform.gaddress.data,
            
            sid = guarantorform.sid.data
        )
        
        db.session.add(guarantor)
        print(guarantor)
        db.session.commit()
        
        
        flash('Guarantor Information saved!', 'success')
        return redirect(url_for('application'))

    return render_template('guarantorform.html', form=guarantorform)

# The University route is where the user will input information relating to their university.
# This is where the user's tuition and major are collected. 
@app.route('/university', methods=['POST', 'GET'])
def universityForm():
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))

    # Instantiate your form class
    universityform= UniversityForm()
    # Validate file upload on submit
    if request.method == 'POST' and universityform.validate_on_submit():
        university = University( 
            sid = universityform.sid.data,
            university_name= universityform.university_name.data,
            student_major = universityform.student_major.data,
            student_faculty= universityform.student_faculty.data,
            student_tuition= universityform.student_tuition.data
            
        )
        
        db.session.add(university)

        db.session.commit()
        
        
        flash('University Information saved!', 'success')
        return redirect(url_for('application'))

    return render_template('universityform.html', form=universityform)


# This route is where the user is able to add new loans to their account.
@app.route('/loanForm', methods=['POST', 'GET'])
def graphicalAnalytics():

    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))

    # Instantiate your form class
    loanForm= LoanForm()

    if request.method == 'POST' and loanForm.validate_on_submit():
       
        loandata = Loan( 
            loan_type = loanForm.loan_type.data,
            loan_status = loanForm.loan_status.data,
            sid = loanForm.sid.data,
            length = loanForm.length.data,
            interestrate = loanForm.interestrate.data,
            loanamount = loanForm.loanamount.data,
            start_date = loanForm.start_date.data,
            moratorium = loanForm.moratorium.data
        )
        
        # Error here, new rows in database, need to migrate.
                
        db.session.add(loandata)
        print(loandata)
        db.session.commit()
        
        flash('Loan Information saved!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('graphicalanalyticsform.html', form=loanForm)

# This is the route where the ADMIN will be able to approve a loan for the user, inputting
# details relating to their loan.
@app.route('/loanAdmin', methods=['POST', 'GET'])
def adminLoan():

    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))

    # Instantiate your form class
    
    loanapp = LoanApplication.query.filter(LoanApplication.id==session['id']).first()
    unidata = University.query.filter(University.sid==str(loanapp.sid)).first()

    loanapplicant = [loanapp.id, session['applicantname'], loanapp.trn, loanapp.sid, loanapp.sex, loanapp.phonenumber, loanapp.email]
    uni = [unidata.university_name, unidata.student_major, unidata.student_tuition]
    imgname = loanapp.photo
    studentsid = loanapp.sid

    loanForm = LoanForm(obj=loanapp)
    imageList=get_uploaded_file()
    imgList = []
    for image in imageList:
        if imgname in image:

            imgList.append(image)

    
    if request.method == 'GET':
        loanForm.loan_type.data = "Student Loan"
        loanForm.loan_status.data = "Ongoing"
        loanForm.moratorium.data = "No"
        
    
    if request.method == 'POST':
        raw = request.form['submit']
            
        loanid, status = raw.split("_")
        
        loanForm.populate_obj(loanapp)
        
        loandata = Loan( 
            loan_type = loanForm.loan_type.data,
            loan_status = loanForm.loan_status.data,
            sid = loanForm.sid.data,
            length = loanForm.length.data,
            interestrate = loanForm.interestrate.data,
            loanamount = loanForm.loanamount.data,
            start_date = loanForm.start_date.data,
            moratorium = loanForm.moratorium.data
        )

        db.session.add(loandata)

        
        if status == 'Approved':
                record = LoanApplication.query.filter(LoanApplication.id == loanid).first()
                record.status = "Approved"
        db.session.commit()
        flash('Loan Approved!', 'success')
        return redirect(url_for('adminDashboard'))
    
    return render_template('graphicalanalyticsform.html', form=loanForm, uni = uni,  loanapp = loanapplicant, applicantname = session['applicantname'], imageList = imgList)


# This route is where the priority of the loans that the user has is displayed.
# Given that the user has multiple loans, the system prioritizes the loan with the highest
# interest accrued. This is the Debt Avalanche method of repayment.
@app.route('/loananalyticsprioritizerform', methods=['POST', 'GET'])
def loanAnalyticsPrioritizer():
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))

    # Instantiate your form class
    loananalyticsprioritizerform=LoanAnalyticsPrioritizerForm()

    if request.method == 'POST' and loananalyticsprioritizerform.validate_on_submit():
       
        loananalyticsprioritizer = LoanPrioritization( 
            loanid = loananalyticsprioritizerform.loanid.data,
            priority_id = loananalyticsprioritizerform.priorityid.data,
            interest= loananalyticsprioritizerform.interest.data
        )
        
       
        db.session.add(loananalyticsprioritizer)
        print(loananalyticsprioritizer)
        db.session.commit()
        flash('added')
        
        flash('File Saved', 'success')
        return redirect(url_for('home'))

    return render_template('loananalyticsprioritizerform.html', form=loananalyticsprioritizerform)


# The ADMIN dashboard is where the ADMIN is able to see all applications. They are
# able to accept applicants or deny them here. After Accepting and applicant, the ADMIN
# must navigate to the review route (Accept, Decline), to complete their job.
@app.route('/admin_dashboard', methods = ['POST', 'GET'])
def adminDashboard():
    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))
    
    if not session.get('is_admin'):
        flash('You are not an Admin! Please login to your account.', 'danger')
        return redirect(url_for('login'))
    
    date = datetime.now()
    print(date)

    
    loanapplicants = LoanApplication.query.all()
    declined = "You declined an applicant: "
    accepted = "You accepted an applicant: "
    undo = "You undid an applicant's status: "
    if request.method == 'POST':
        
        if (request.form['submit'] == 'Accepted') or (request.form['submit'] == 'Declined') or (request.form['submit'] == 'Approved'):
            condition = request.form['submit']
            print(f"review condition: {condition}")
            return render_template('review.html', loanapplicants = loanapplicants, condition = condition)  
        
        else:
            raw = request.form['submit']
            
            loanid, status = raw.split("_")

            loanapp = LoanApplication.query.filter(LoanApplication.id==loanid).first()
            print(loanapp)
            applicantname= loanapp.first_name + " " + loanapp.last_name
            
            if status == 'Accept':
                record = LoanApplication.query.filter(LoanApplication.id == loanid).first()
                record.status = "Accepted"
                print("i accepted")
                flash(f'Notice! {accepted} {applicantname} ID: {loanid}', 'success')

                adminlogdata = AdminLog(
                    logdata = f"Notice! {accepted} {applicantname} ID: {loanid}",
                    time = datetime.now()
                )
                
                db.session.add(adminlogdata)
                
                db.session.commit()

                return redirect(url_for('adminDashboard'))  
            if status == 'Decline':
                flash(f'Notice! {declined} {applicantname} ID: {loanid}', 'danger') 
                # LoanApplication.query.filter(LoanApplication.id == loanid).delete()
                record = LoanApplication.query.filter(LoanApplication.id == loanid).first()
                record.status = "Declined"
                print("i think i declined")
                
                adminlogdata = AdminLog(
                    logdata = f"Notice! {declined} {applicantname} ID: {loanid}",
                    time = datetime.now()
                )
                
                db.session.add(adminlogdata)
                
                db.session.commit()
                return redirect(url_for('adminDashboard'))
            
            if status == 'Undo':
                flash(f'Notice! {undo} {applicantname} ID: {loanid}', 'danger') 
                # LoanApplication.query.filter(LoanApplication.id == loanid).delete()
                record = LoanApplication.query.filter(LoanApplication.id == loanid).first()
                record.status = "Waiting"
                print("i think i undid")
                
                adminlogdata = AdminLog(
                    logdata = f"Notice! {undo} {applicantname} ID: {loanid}",
                    time = datetime.now()
                )
                db.session.add(adminlogdata)
                
                db.session.commit()
                return redirect(url_for('adminDashboard'))
            
            if status == 'Approve':

                
                session['tsid'] = loanapp.sid
                session['id'] = loanapp.id
                session['applicantname'] = applicantname
                

                return redirect(url_for('adminLoan'))
        # if request.form['review']:
            
                 
    
    return render_template('adminDashboard.html', loanapplicants =loanapplicants)

# All actions taken by the ADMIN on the ADMIN DASHBOARD are stored to the database to keep
# track of any movements they make.
@app.route('/log')
def adminLog():

    if not session.get('logged_in'):
        flash('You are not logged in! Please log in and try again.', 'danger')
        return redirect(url_for('login'))

    log = AdminLog.query.order_by(desc(AdminLog.time)).all()

    

    return render_template('adminlog.html', adminlog=log)

# This function grabs the images uploaded to the system.
def get_uploaded_file():
    rootdir = os.getcwd()
    upload_files=[]
    for subdir, dirs, files in os.walk(rootdir + '/uploads'):    
        for file in files:
        
            upload_files.append(file)
    upload_files.pop(0)     
    return upload_files

@app.route('/uploads/<filename>')
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

#
@app.route('/files')
def files():
    imgs=get_uploaded_file()
    return render_template('files.html', imgs=imgs)

# The login route is pretty much self explanatory. This is the standard
# login page for our user. If the admin inputs his credentials here, they are
# logged in straight to the admin dashboard from this route.
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    
    if request.method == 'POST':
        
        if request.form['username'] == 'admin':
            if request.form['password'] == 'admin':
                session['is_admin'] = True
                session['logged_in'] = True
                flash('welcome Admin', 'success')
                return redirect(url_for('adminDashboard'))
                
        if request.form['username']:
            username = request.form['username']
            password = request.form['password']
            
            user = SignUpProfile.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password, password):
                session['logged_in'] = True
                session['is_student'] = True
                flash('Successfully logged in', 'success')
                searchstudentid = SignUpProfile.query.all()
                

                for x in searchstudentid:
                    if x.username == username:
                        sid = x.sid
                        usrname = x.first_name + " " + x.last_name
                        

                print("your sid is: ", sid)
                print("username is: ", usrname)
                session['username'] = usrname
                session['sid'] = sid
                print("welp session id: ", session['sid'])
                return redirect(url_for('home'))
            
            else:
                error = 'Invalid username or password'

                
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('is_admin', None)
    session.pop('is_student', None)
    flash('You were logged out', 'success')
    return redirect(url_for('home'))


###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('home.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")