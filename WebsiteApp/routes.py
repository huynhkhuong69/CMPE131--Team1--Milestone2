from datetime import datetime
import time
import pyttsx3

from flask import *  # Imports all the functions at once (render_template,flash,etc.)
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message
from werkzeug.security import generate_password_hash
from werkzeug.wrappers import response

from WebsiteApp import app_Obj, db, mail
from WebsiteApp.forms import (LoginForm, RegisterForm, SettingsForm, ToDoListForm, create_FlashCardsForm , pomorodoTimerForm )
from WebsiteApp.models import FlashCards, ToDoList, User

from bs4 import BeautifulSoup
import requests

@app_Obj.route('/')
@app_Obj.route('/home')
def homePage():
    return render_template('home.html')

@app_Obj.route("/register", methods= ['GET', 'POST'])
def registerPage():
    title = "Registration Page"
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
    return render_template ("register.html", form = form,title=title)             

@app_Obj.route("/login", methods=['GET', 'POST'])
def loginPage():
    title = "Login Page"
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login invalid username or password!')
            return redirect('/login')

        login_user(user, remember=form.remember_me.data)
        flash(f'Successfull Login for requested user {form.username.data} at {time.strftime("%H:%M:%S")}')
        return redirect('/')

    return render_template("login.html", form=form,title=title)

@app_Obj.route("/logout", methods=['GET', 'POST'])
@login_required
def logoutPage():
    logout_user()
    flash('You have successfully logged out!')
    return redirect('/login')

@app_Obj.route("/settings", methods=['GET', 'POST'])
@login_required
def user_SettingsPage():
    title = "Setting Page"
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
    return render_template('settings.html',form=form,title=title)

@app_Obj.route ('/todolist', methods = ['GET', 'POST'])
def todolistPage():
    form = ToDoListForm()
    title = "To-Do-List"
    if request.method == 'POST':
        task_content = request.form['task_name']
        new_task = ToDoList(task_name = task_content)
        try:
            db.session.add (new_task)
            db.session.commit()
            return redirect('/todolist')
        except:
            return flash ('Error: could not add a task')
    else:
        tasks = ToDoList.query.all()
        return render_template ("todolist.html", tasks = tasks, form=form,title=title)

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
    title = "Update Task"
    task = ToDoList.query.get_or_404(id)
    if request.method == 'POST':
        task.task_name = request.form['task_name']
        try:
            db.session.commit()
            return redirect ('/todolist')
        except:
            return flash('Error: could not update a task')
    else:
        return render_template('update.html', task = task, form=form,title=title) 

## Youhao's work
## Add Time spend on Assignment feature
@app_Obj.route ('/start/<int:id>', methods = ['GET', 'POST'])
def start(id):
    form = ToDoListForm()
    title = "Start Task"
    task = ToDoList.query.get_or_404(id)
    if request.method == 'POST':
        task.task_name = request.form['task_name']
        try:
            db.session.commit()
            return redirect ('/todolist')
        except:
            return flash('Error: could not update a task')
    else:
        return render_template('start.html', task = task, form=form,title=title) 

@app_Obj.route('/create-edit-flashcards/', methods = ['GET', 'POST'])
def create_flashcards():
    form = create_FlashCardsForm()
    title = "Create-Edit Flash Cards"

    if form.validate_on_submit():
        new_flashCard = FlashCards(flashCard_name = form.flashcard_name.data, flashCard_description = form.flashcard_description.data, flashCard_hint=form.flashcard_hint.data)
        try:
            db.session.add(new_flashCard)
            db.session.commit()
            return redirect('/create-edit-flashcards')
        except:
            return flash ('Error: Unable to save Flash Card!')
    else:
        flashcards = FlashCards.query.all()
        return render_template('flashcard.html',form=form, flashcards=flashcards,title=title) 

@app_Obj.route('/delete-flashcard/<int:id>')
def delete_flashCard(id):
    delete_flashCard = FlashCards.query.get_or_404(id)
    try:
        db.session.delete(delete_flashCard)
        db.session.commit()
        return redirect ('/create-edit-flashcards')
    except:
        return flash ('Error: Unable to delete Flash Card!')
    
@app_Obj.route('/edit-flashcard/<int:id>', methods = ['GET', 'POST'])
def edit_flashCard(id):
    update_flashCard = FlashCards.query.get_or_404(id)
    title = "Update Flash Card"
    if request.method == 'POST':
        update_flashCard.flashCard_name = request.form['flashCard_name']
        update_flashCard.flashCard_description = request.form['flashCard_description']
        try:
            db.session.commit()
            return redirect ('/create-edit-flashcards')
        except:
            return flash('Error: could not update a flashcard')
    else:
        return render_template('update_flashcard.html', update_flashCard = update_flashCard, title=title) 

@app_Obj.route('/view-flashcards')
def view_flashCards():
    title = 'View Flash Cards'
    flashcards = FlashCards.query.all()
    return render_template('view_flashcards.html',flashcards=flashcards, title=title)

@app_Obj.route('/send_message', methods=['GET', 'POST'])
def send_message():
    title = 'Send an Email'
    if  request.method == "POST":
        try:
            email = str(request.form['email'])
            subject = str(request.form['subject'])
            msg_body = str(request.form['message'])

            message = Message(subject, sender="teamonecmpe131@gmail.com", recipients=[email])
            message.body = msg_body
            mail.send(message) #Sends email
            flash("Email Sent!")
            return redirect('/')
            
        except ConnectionRefusedError as connectionRefusedError_:
            return "Failed to send Email. Please try again later!"
    else:
        return render_template("email.html",title=title)

@app_Obj.route('/share-flashcards', methods=['POST'])
def share_flashCards():
    flashcards = FlashCards.query.all()
    if request.method == "POST":
        try:
            email = str(request.form['email'])
            subject = 'Flash Cards'
            message = Message(subject, sender="teamonecmpe131@gmail.com", recipients=[email])
            message.body = render_template("share_flashcards.html",flashcards=flashcards)
            message.html = render_template("share_flashcards.html",flashcards=flashcards)
            message.attach = render_template("share_flashcards.html",flashcards=flashcards)
            mail.send(message) #Sends email
            flash("Flashcards Email Sent!")
            return redirect('/')
            
        except ConnectionRefusedError as connectionRefusedError_:
            return "Failed to send Email. Please try again later!"
    else:
        return render_template("view_flashcards.html")

@app_Obj.route('/timer', methods = ['GET', 'POST'])
def pomodoro ():
    form = pomorodoTimerForm()
    title = 'Start a Timer'
    if request.method == 'POST':
        try: 
            study_time = (request.form ["study_time"])
            #break_time = (request.form ["break_time"])
            timer (int(study_time))
            return redirect ("/timer")
        except:
            return flash ('Fail to load timer')
    else: 
        return render_template ("timer.html", form = form,title=title)

def timer (t):
    # t = 25*60
    while t:
        mins, secs = divmod (t, 60)
        timer = '{:02d}: {:02d}'.format (mins, secs)
        print (timer, end = "\r")
        time.sleep(1)
        t -=1
    pyttsx3.speak ("beep beep beep beep time to work")
    return t

@app_Obj.route('/api/image-search/<string:keyword>', methods=['GET'])
def imageSearch(keyword):
    response = requests.get(f'https://www.google.com/search?q={keyword}&tbm=isch')
    bs = BeautifulSoup(response.text, 'lxml')
    srcList = []
    for src in bs.find_all('img'):
        if('http' in src['src']):
            srcList.append(src['src'])
        else:
            pass
    json_data = json.dumps(srcList)
    return json_data