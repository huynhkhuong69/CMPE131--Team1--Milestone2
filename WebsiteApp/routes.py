from flask import *  # Imports all the functions at once (render_template,flash,etc.)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash
from wtforms.validators import Email

from WebsiteApp import app_Obj, db
from WebsiteApp.forms import LoginForm, RegisterForm
from WebsiteApp.models import User

@app_Obj.route('/')
@app_Obj.route('/home')
def homePage():
    return render_template('home.html')

@app_Obj.route("/register", methods= ['GET', 'POST'])
def registerPage():
    form = RegisterForm()

    user = User.query.filter_by(email=form.email.data).first()

    if user is not None:
        flash('Email already exists!')
        return redirect ('/register')

    if form.validate_on_submit():
        if not request.form ['email'] or not request.form ['username']:
            flash('Please enter your username or email')
        if request.form['password'] != request.form['confirmPassword']:
            flash('Password do not match!')
        else:
            hashed_password = generate_password_hash(form.password.data, 'sha256')
            new_user = User(username = form.username.data, email = form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('New member was successfully added')
            return redirect ('/login')
    return render_template ("register.html", form = form)             

@app_Obj.route("/login", methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login invalid username or password!')
            return redirect('/login')

        login_user(user, remember=form.remember_me.data)
        flash(f'Successfull Login for requested for user {form.username.data}')
        return redirect('/')

    return render_template("login.html", form=form)
