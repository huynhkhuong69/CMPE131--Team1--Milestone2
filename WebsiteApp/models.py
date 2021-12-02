from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from WebsiteApp import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    password  = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

class ToDoList(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_name = db.Column(db.String(64))
    complete = db.Column(db.Boolean)

    def __repr__ (self):
        return f'<Task {self.id} : {self.task_name}>'

class FlashCards(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    flashCard_name = db.Column(db.String(256))
    flashCard_description = db.Column(db.String(512))
    flashCard_hint = db.Column(db.String(64))
    flashCard_image = db.Column(db.String(64))

    def __repr__(self):
        return f'<FlashCard {self.id} : {self.flashCard_name}><Image: {self.flashCard_image}>'

class Note(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(1024), index=True)
    share_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Id: {self.id} |{self.note}|'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
