# Login Form Stuff should go here
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets.core import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')
    
class RegisterForm(FlaskForm):
    username = StringField ('Username', validators = [DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password',validators = [DataRequired()])
    confirmPassword = PasswordField ('Confirm Password',validators = [DataRequired()])
    register_button = SubmitField('Register')

class SettingsForm(FlaskForm):
    delete_account = StringField('Delete Account',validators = [DataRequired()])
    submit = SubmitField('Delete Account')
    
class ToDoListForm(FlaskForm):
    task_name = StringField ('Enter a task', validators = [DataRequired()])
    add_task_button = SubmitField('Add task')

class create_FlashCardsForm(FlaskForm):
    flashcard_name = StringField('Flash Card Name', validators = [DataRequired()])
    flashcard_description = StringField('Flash Card Description', validators = [DataRequired()], widget=TextArea() ,render_kw={'style': 'width: 500px'},)
    flashcard_hint = StringField('Flash Card Hint', validators = [DataRequired()])
    save_flashCard = SubmitField('Save Flash Card')


class pomorodoTimerForm (FlaskForm):
    study_time = IntegerField('Study Time', validators = [DataRequired()])
    # break_time = IntegerField('Break Time', validators = [DataRequired()])
    start_button = SubmitField('Start')
    # reset_button = SubmitField('Reset')

class noteForm (FlaskForm):
    file = FileField('Choose file to upload')
    submit = SubmitField('Upload')
    