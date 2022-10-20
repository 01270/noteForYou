from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('routes.home'))
            else: flash("Wrong password!", category="error")
        else: flash("Email not found!", category="error")
    return render_template("login.html", login_user=None)

@auth.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        user = User.query.filter_by(email=email).first()
        if user: flash("Email already used!", category="error")
        elif len(email) < 4: flash("Email is too short!", category="error")
        elif len(firstName) < 3: flash("Name must be greater than 2 character", category="error")
        elif len(password1) < 5: flash("Password is too short!", category="error")
        elif password1 != password2: flash("Password dosn't math!", category="error")
        else: 
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for('routes.home'))
    return render_template("signup.html", login_user=None)