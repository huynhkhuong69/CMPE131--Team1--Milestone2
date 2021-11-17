from flask import *  # Imports all the functions at once (render_template,flash,etc.)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.validators import Email

from WebsiteApp import app_Obj, db
from WebsiteApp.forms import LoginForm, RegisterForm, SettingsForm, ToDoListForm, create_FlashCardsForm
from WebsiteApp.models import User, ToDoList, FlashCards

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
        new_task = ToDoList(task_name = task_content)
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

@app_Obj.route('/create-edit-flashcards', methods = ['GET', 'POST'])
def create_flashcards():
    form = create_FlashCardsForm()
    if form.validate_on_submit():
        new_flashCard = FlashCards(flashCard_name = form.flashcard_name.data, flashCard_description = form.flashcard_description.data)
        try:
            db.session.add(new_flashCard)
            db.session.commit()
            return redirect('/create-edit-flashcards')
        except:
            return flash ('Error: Unable to save Flash Card!')
    else:
        flashcards = FlashCards.query.all()
        return render_template('flashcard.html',form=form, flashcards=flashcards) 

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
    print(update_flashCard)
    if request.method == 'POST':
        update_flashCard.flashCard_name = request.form['flashCard_name']
        update_flashCard.flashCard_description = request.form['flashCard_description']
        try:
            db.session.commit()
            return redirect ('/create-edit-flashcards')
        except:
            return flash('Error: could not update a flashcard')
    else:
        return render_template('update_flashcard.html', update_flashCard = update_flashCard) 

@app_Obj.route('/view-flashcards')
def view_flashCards():
    flashcards = FlashCards.query.all()
    return render_template('view_flashcards.html',flashcards=flashcards)

@app_Obj.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if  request.method == "POST":
        email = request.form['email']
        subject = request.form['subject']
        msg = request.form['email']

        db.session.commit()

        message = Message('subject', sender="huynhkhuong8203@gmail.com", recipients=[email])
        message.body = msg

        mail.send(message)
        success = "Message Sent"
    else:
        return render_template("email.html", send_message=send_message)
