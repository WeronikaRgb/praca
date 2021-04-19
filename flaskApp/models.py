from flaskApp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Quiz(db.Model):
    __tablename__ = 'quiz'
    def __init__(self, question):
        self.question = question
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String())
    good_answer = db.Column(db.String())
    bad_answer = db.Column(db.String())
    bad_answer2 = db.Column(db.String())