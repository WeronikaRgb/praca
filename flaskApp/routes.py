import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskApp import app, db, bcrypt
from flaskApp.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskApp.models import User, Quiz
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def hello_world():
    return 'Hello Worldddd!'


@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/szczyty')
def szczyty():
    return render_template('szczyty.html')


@app.route('/kzkgp')
def kzkgp():
    return render_template('kzkgp.html')


@app.route('/ciekawostki')
def ciekawostki():
    return render_template('ciekawostki.html')


@app.route('/quiz')
def quiz():
    return render_template('quiz.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Utworzono konto! Zaloguj się.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('start'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('start'))
        else:
            flash('Logowanie nie powiodło się. Sprawdź email i hasło!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('start'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/konto", methods=['GET', 'POST'])
@login_required
def konto():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Twoje konto zostało zaktualizowane!', 'success')
        return redirect(url_for('konto'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('konto.html', title='Account', image_file=image_file, form=form)




# class Player:
#     def __init__(self, name):
#         self.name = name
#     punkty = 0

# konfiguracja aplikacji
# app.config.update(dict(
#     SECRET_KEY='bradzosekretnawartosc',
# ))

# lista pytań
# DANE = [{
#     'pytanie': 'Ile szczytów liczy Korona Gór Polski?',  # pytanie
#     'odpowiedzi': ['28', '38', '48'],  # możliwe odpowiedzi
#     'odpok': '28'},  # poprawna odpowiedź
#     {
#     'pytanie': 'Jaki jest najniższy szczyt KGP?',
#     'odpowiedzi': ['Czupel', 'Łysica', 'Lackowa'],
#         'odpok': 'Łysica'},
#     {
#     'pytanie': 'Jaki jest najwyższy szczyt KGP?',
#     'odpowiedzi': ['Rysy', 'Śnieżka', 'Babia Góra'],
#     'odpok': 'Rysy'},
#     {
#     'pytanie': 'W jakim paśmie leżą Rysy?',
#     'odpowiedzi': ['Tatry', 'Bieszczady', 'Karkonosze'],
#     'odpok': 'Tatry'},
# ]
#
#
# @app.route('/gra', methods=['GET', 'POST'])
# def gra():
#     if request.method == 'POST':
#         punkty = 0
#         odpowiedzi = request.form
#
#
#         for pnr, odp in odpowiedzi.items():
#             if odp == DANE[int(pnr)]['odpok']:
#                 punkty += 1
#
#         flash('Liczba poprawnych odpowiedzi, to: {0}'.format(punkty))
#         return redirect(url_for('gra'))
#     return render_template('gra.html', pytania=DANE)
