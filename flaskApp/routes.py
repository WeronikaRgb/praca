import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskApp import app, db, bcrypt
from flaskApp.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskApp.models import User, Quiz, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app)

class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)
       # return current_user.is_authenticated

    def not_auth(self):
        return "you are not auth"


admin.add_view(Controller(Quiz, db.session))
admin.add_view(Controller(User, db.session))
admin.add_view(Controller(Post, db.session))


class MyView:
    def is_accessible(self):
        return login.current_user.is_authenticated()


@app.route('/koniecgry')
def koniecgry():
    return render_template('koniecgry.html')


@app.route('/')
def start():
    return render_template('start.html')

@app.route('/ostronie')
def ostronie():
    return render_template('ostronie.html')

@app.route('/galeria')
def galeria():
    posts = Post.query.all()
    return render_template('galeria.html', posts=posts)

@app.route('/szczyty')
def szczyty():
    return render_template('szczyty.html')


@app.route('/kzkgp')
def kzkgp():
    return render_template('kzkgp.html')



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


def save_picture(form_picture, pic_path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, pic_path , picture_fn)

    output_size = (750, 700)
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
            picture_file = save_picture(form.picture.data, 'static/profile_pics/')
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



app.config['SECRET_KEY'] = 'bradzosekretnawartosc'


@app.route('/gra', methods=['GET', 'POST'])
def gra():
    questions = Quiz.query.all()

    results = [
        {
            "Question": question.question,
            "Answers": [question.answer1, question.answer2, question.answer3],
            "GoodAnswer": question.good_answer,
            "ID": question.id
        } for question in questions]

    if request.method == 'POST':
        punkty = 0
        odpowiedzi = request.form

        for pnr, odp in odpowiedzi.items():
            if odp == results[int(pnr)]['GoodAnswer']:
                punkty += 1

        flash('Liczba poprawnych odpowiedzi, to: {0}'.format(punkty))
        return redirect(url_for('gra'))

    return render_template('gra.html', questions=questions, quiz=results)






@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_picture(form.image_file.data, 'static/gallery_pics/')
        post = Post(title=form.title.data, content=form.content.data, image_file=picture_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('galeria'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='Nowy Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/hej')
def hej():
    return render_template('hej.html')




@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
     post = Post.query.get_or_404(post_id)
     if post.author != current_user:
         abort(403)
     db.session.delete(post)
     db.session.commit()
     flash('Twój post został usunięty!', 'success')
     return redirect(url_for('galeria'))
