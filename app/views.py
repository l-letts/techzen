"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from werkzeug.utils import secure_filename
from .forms import *
# from flask_mysqldb import MySQL
# import mysql.connector

###
# Routing for your application.
###
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="",
#     db="dev_techzen_db"
# )

# my_cursor = mydb.cursor()

@app.route('/home')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="TechZen")

@app.route('/register', methods=['POST', 'GET'])
def register():
    # if not session.get('logged_in'):
    #     abort(401)

    # Instantiate your form class
    registerform=SignUpForm()
    # Validate file upload on submit
    if request.method == 'POST' and registerform.validate_on_submit():
        # fname = request.form['fname']
        # lname = request.form['lname']
        # username = request.form['username']
        # email = request.form['email']
        # password = request.form['password']
        
        # my_cursor.execute("INSERT INTO studentssignup VALUES(%s,%s,%s,%s,%s)", (fname,lname,username,email,password))
        # mydb.connection.commmit()
        # my_cursor.close()        
        # Get file data and save to your uploads folder
        # filename=secure_filename(photo.filename)
        # photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File Saved', 'success')
        return redirect(url_for('home'))

    return render_template('signup.html', form=registerform)

@app.route('/apply', methods=['POST', 'GET'])
def loanApplication():
    # if not session.get('logged_in'):
    #     abort(401)

    # Instantiate your form class
    applicationform=LoanApplicationForm()
    # Validate file upload on submit
    if request.method == 'POST' and applicationform.validate_on_submit():
        # Get file data and save to your uploads folder
        photo=applicationform.image.data

        # filename=secure_filename(photo.filename)
        # photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File Saved', 'success')
        return redirect(url_for('home'))

    return render_template('loanapplication.html', form=applicationform)

@app.route('/guarantor', methods=['POST', 'GET'])
def guarantorForm():
    # if not session.get('logged_in'):
    #     abort(401)

    # Instantiate your form class
    guarantorform= GuarantorForm()
    # Validate file upload on submit
    if request.method == 'POST' and guarantorform.validate_on_submit():
        flash('Form Completed', 'success')
        return redirect(url_for('home'))

    return render_template('guarantorform.html', form=guarantorform)

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


@app.route('/files')
def files():
    imgs=get_uploaded_file()
    return render_template('files.html', imgs=imgs)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['ADMIN_USERNAME'] or request.form['password'] != app.config['ADMIN_PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            
            flash('You were logged in', 'success')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
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
