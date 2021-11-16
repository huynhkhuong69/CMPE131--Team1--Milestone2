import os
import flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app_Obj = flask.Flask(__name__) 

#email API documentation 
app_Obj.config['MAIL_SERVER'] = 'smtp.gmail.com'
app_Obj.config['MAIL_PORT'] = 465
app_Obj.config['MAIL_USERNAME'] = "huynhkhuong8203@gmail.com" #use ur email
app_Obj.config['MAIL_PASSWORD'] = "Enter your pw here"
app_Obj.config["MAIL_USE_TLS"] = False
app_Obj.config['MAIL_USE_SSL'] = True

mail = Mail(app_Obj)


app_Obj.config.from_mapping (
    SECRET_KEY = 'it-dont-matter',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app_Obj)
login = LoginManager(app_Obj)
login.login_view = 'loginPage'

from WebsiteApp import routes, models
