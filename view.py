# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, render_template, flash
from flask import redirect
from flask import request
from flask import url_for
from model import *
import os
import inspect
import re
from flask_login import LoginManager, UserMixin, login_required, \
    login_user, logout_user, current_user

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'bmp'}

app = Flask(__name__)
app.config.update(
    SECRET_KEY="python_class"
)
app.config['TESTING'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


error = ''


@app.route('/', methods=["POST", "GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('.dashboard'))
    return render_template("index.html")


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        print('*******  {}  ********'.format(inspect.stack()[0][3]))
        form = request.form
        first_name, last_name, email, password = form.get('first_name'), form.get('last_name'), form.get(
            'email'), form.get('password')
        if first_name and last_name and email and password:
            if is_valid_email(email):
                if check_email_uniqueness(email):
                    add_user(first_name, last_name, email, password)
                    id = get_user_id(email, password)
                    user = User(id)
                    login_user(user)
                    return redirect(url_for('.dashboard'))
                else:
                    flash('ایمیل ورودی تکراری است!', category='signup')
            else:
                flash('ایمیل معتبر نیست!', category='signup')
        else:
            flash("تمام فیلدها را پر کنید!", category='signup')

    return redirect('/')


@app.route('/signin', methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        print('*******  {}  ********'.format(inspect.stack()[0][3]))
        form = request.form
        email, password = form.get('email'), form.get('password')
        if email and password:
            if authenticate_user(email, password):
                id = get_user_id(email, password)
                user = User(id)
                login_user(user)
                return redirect(url_for('.dashboard'))
            else:
                flash('ایمیل یا کلمه عبور اشتباه است!', category='signin')
        else:
            flash("تمام فیلدها را پر کنید!", category='signin')
    return redirect("/")


@app.route('/signout', methods=["POST", "GET"])
@login_required
def signout():
    if request.method == "POST":
        logout_user()
        return redirect("/")
    return redirect("/")


@app.route('/dashboard', methods=["POST", "GET"])
@login_required
def dashboard(user=''):
    print('*******  {}  ********'.format(inspect.stack()[0][3]))
    if request.method == "POST":
        form = request.form

    if request.method == "GET":
        id = current_user.id
        user = get_user_by_id(id)

    return render_template("dashboard.html", user=user)


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload(user=''):
    print('*******  {}  ********'.format(inspect.stack()[0][3]))
    if request.method == "POST":
        file = request.files['file']

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.id)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        file.save(os.path.join(upload_path, file.filename))

    return render_template("dashboard.html", user=user)


@app.route('/change_password', methods=["POST", "GET"])
@login_required
def change_password():
    print('*******  {}  ********'.format(inspect.stack()[0][3]))
    if request.method == "POST":
        form = request.form
        oldPass, newPass, newPass_repeat = form.get('oldPass'), form.get('newPass'), form.get('newPass_repeat')
        if oldPass and newPass and newPass_repeat:
            if authenticate_user_by_id(current_user.id, oldPass):
                if newPass == newPass_repeat:
                    change_user_password(current_user.id, newPass)
                else:
                    flash('!تکرار رمز مطابق نیست')
            else:
                flash('!رمز قبلی اشتباه وارد شده است')
        else:
            flash('!تمام فیلدها را پر کنید')

    return redirect(url_for('.dashboard'))


def is_valid_email(email):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is not None:
        return True
    return False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(port=8082, debug=True)
