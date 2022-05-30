import email
import errno
from flask import Blueprint, render_template, request, flash, redirect, url_for
from xmlrpc.client import boolean
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

# methods signifies that this route accept GET and POST requests. Will only be defaulted to GET if not specified.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Searching for specific entry in the database and return the first one
        user = User.query.filter_by(email=email).first()
        # If user is found, check to see if the password matches the hashed password in the database
        if user:
            if check_password_hash(user.password, password):
                flash('You have successfully logged in', category='success')
                # Remembers that the user is logged
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else: 
            flash('Email does not exist', category='error')
                      
    return render_template("login.html", user=current_user)

@auth.route('/logout')
# Cannot access this route unless the user is logged in
@login_required
def logout():
    # Returns user to the login page when they logout
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    # flash is  a built in function that will display a message to the user provided by flask
    # If user exists in the db, flash error message
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else: 
            # add user to the database                                              sha256 is a hashing algorithm                        
            new_user = User(email=email, first_name=first_name, 
                            password=generate_password_hash(password1, 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            # Remembers that the user is logged
            login_user(user, remember=True)
            flash('Account created!', category='success')
            # Redirect to home page
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)