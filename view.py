# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from flask import Flask, render_template, flash, send_file
from flask import redirect
from flask import request
from flask import url_for
from model import *
import os
import inspect
import re
from flask_login import LoginManager, UserMixin, login_required, \
    login_user, logout_user, current_user
import socket

host = 'localhost'
port = 1027
server_address = (host, port)

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
                    flash('!تکرار رمز مطابق نیست', category='pass')
            else:
                flash('!رمز قبلی اشتباه وارد شده است', category='pass')
        else:
            flash('!تمام فیلدها را پر کنید', category='pass')

    return redirect(url_for('.dashboard'))


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    print('*******  {}  ********'.format(inspect.stack()[0][3]))
    if request.method == "POST":

        file = request.files['file']
        filename = file.filename
        print(filename)

        history_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.id)
        if not os.path.exists(history_path):
            os.makedirs(history_path)

        record_id = get_record_id(history_path)
        record_path = os.path.join(history_path, record_id)
        os.makedirs(record_path)

        file.save(os.path.join(record_path, filename))

        ocr_request(record_path, filename)

        _, file_type = os.path.splitext(filename)
        out_file = os.path.join(record_path, 'out_text.txt')

        add_record(current_user.id, filename, file_type, os.path.join(record_path, filename), out_file)

        flash('step3', category='step3')

    return redirect(url_for('.dashboard'))

@app.route('/download', methods=["POST", "GET"])
@login_required
def download():
    print('*******  {}  ********'.format(inspect.stack()[0][3]))
    if request.method == "POST":

        out_text_path = get_last_out_text(current_user.id)

        return send_file(out_text_path,
                         attachment_filename='out_text.txt')

    return redirect(url_for('.dashboard'))


@app.route('/history', methods=["POST", "GET"])
@login_required
def history():
    print('*******  {}  ********'.format(inspect.stack()[0][3]))
    if request.method == "POST":
        pass

    if request.method == "GET":
        id = current_user.id
        user = get_user_by_id(id)

        results = get_history(current_user.id)


    return render_template("history.html", user=user, results=results)


def is_valid_email(email):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email) is not None:
        return True
    return False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def ocr_request(record_path, filename):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    print('connected to {}'.format(server_address))

    sock.send(filename.encode())

    data = sock.recv(1024)
    print('client received', repr(data))

    f = open(os.path.join(record_path, filename), 'rb')
    l = f.read(1024)
    while l:
        sock.send(l)
        # print('Sent ', repr(l))
        l = f.read(1024)
    f.close()

    sock.close()
    print('Done sending')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

    sock.send(b'wait for receive from server')

    with open(os.path.join(record_path, 'out_text.txt'), 'wb') as f:
        print('file opened')
        while True:
            print('receiving data...')
            data = sock.recv(1024)
            # print('data=%s', data)
            if not data:
                break
            # write data to a file
            f.write(data)

    f.close()
    print('Successfully get the file')
    sock.close()
    print('connection closed')


def get_record_id(path):
    folders = 0
    for _, dirnames, _ in os.walk(path):
        folders += len(dirnames)
    return str(folders + 1)


if __name__ == "__main__":
    app.run(port=8082, debug=True)
