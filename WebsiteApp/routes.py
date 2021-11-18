from flask import *  # Imports all the functions at once (render_template,flash,etc.)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import Email

from WebsiteApp import app_Obj, db
from WebsiteApp.forms import LoginForm, RegisterForm, SettingsForm, ToDoListForm
from WebsiteApp.models import User, ToDoList
from flask_mail import Mail, Message

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
        flash(f'Successfull Login for requested user {form.username.data}')
        return redirect('/')

    return render_template("login.html", form=form)

@app_Obj.route("/logout", methods=['GET', 'POST'])
@login_required
def logoutPage():
    logout_user()
    flash('You have successfully logged out!')
    return redirect('/login')

@app_Obj.route("/settings", methods=['GET', 'POST'])
@login_required
def user_SettingsPage():
    form = SettingsForm()
    if form.validate_on_submit():
        if(form.delete_account.data != f'Confirm Delete Account {current_user.email}'):
            flash('Unable to delete account')
        else:
            userID = User.query.filter_by(id=current_user.id).first()
            db.session.delete(userID)
            db.session.commit()
            flash('Deleted account. We hope to see you soon!')
            return redirect('/login')
    return render_template('settings.html',form=form)

@app_Obj.route ('/todolist', methods = ['GET', 'POST'])
def todolistPage():
    form = ToDoListForm()
    if request.method == 'POST':
        task_content = request.form['task_name']
        new_task = ToDoList (task_name = task_content)
        try:
            db.session.add (new_task)
            db.session.commit()
            return redirect('/todolist')
        except:
            return flash ('Error: could not add a task')

    else:
        tasks = ToDoList.query.all()
        return render_template ("todolist.html", tasks = tasks, form=form)

@app_Obj.route('/delete/<int:id>')
def delete(id):
    delete_task = ToDoList.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect ('/todolist')
    except:
        return flash ('Error: could not delete a task')

@app_Obj.route ('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = ToDoListForm()
    task = ToDoList.query.get_or_404(id)
    if request.method == 'POST':
        task.task_name = request.form['task_name']
        try:
            db.session.commit()
            return redirect ('/todolist')
        except:
            return flash('Error: could not update a task')
    else:
        return render_template('update.html', task = task, form=form)

@app_Obj.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if  request.method == "POST":
        message = Message('Subject here', sender="noreply@demo.com", recipients=['huynhkhuong8203@gmail.com'])
        message.body = "CMPE131 Project!!!"
        #send email
        mail.send(message)
        #lets user know message is sent
        return "Message Sent"
    return render_template("email.html")

