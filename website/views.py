from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
# Cannot get to the home page unless the user is logged in
@login_required
def home():
    return render_template("home.html")
