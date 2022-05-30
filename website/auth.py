from flask import Blueprint, render_template, request, flash, redirect, url_for
from xmlrpc.client import boolean
from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

# methods signifies that this route accept GET and POST requests. Will only be defaulted to GET if not specified.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    # flash is  a built in function that will display a message to the user provided by flask
        if len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else: 
            # add user to the database
            flash('Account created!', category='success')

    return render_template("sign_up.html")