from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskApp.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zarejestruj')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ta nazwa jest już zajęta. Proszę wybrać inną.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ten email jest już zajęty. Proszę wybrać inny.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nazwa użytkownika',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Zmień zdjęcie profilowe', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class QuestionForm(FlaskForm):
    question = TextAreaField('Pytanie', validators=[DataRequired()])
    submit = SubmitField('Gotowe!')


class PostForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    content = TextAreaField('Komentarz', validators=[DataRequired()])
    image_file = FileField('Zdjęcie ', validators=[FileAllowed(['jpg', 'png']), FileRequired()])
    submit = SubmitField('Opublikuj')