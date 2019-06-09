# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, render_template, flash
from flask import redirect
from flask import request
from flask import url_for
from model import *
import inspect
from flask_login import LoginManager, UserMixin, login_required, \
    login_user, logout_user, current_user

app = Flask(__name__)
app.config.update(
    SECRET_KEY="python_class"
)
app.config['TESTING'] = False

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
    if request.method=="POST":
        print('*******  {}  ********'.format(inspect.stack()[0][3]))
        form = request.form
        first_name, last_name, email, password = form.get('first_name'), form.get('last_name'), form.get('email'), form.get('password')
        # TODO validate inputs
        if first_name and last_name and email and password:
            add_user(first_name, last_name, email, password)
            # TODO Check the uniqueness of the email
            id = get_user_id(email, password)
            user = User(id)
            login_user(user)
            return redirect(url_for('.dashboard'))

    return redirect('/')

@app.route('/signin', methods=["POST", "GET"])
def signin():
    if request.method=="POST":
        print('*******  {}  ********'.format(inspect.stack()[0][3]))
        form = request.form
        email, password = form.get('email'), form.get('password')
        # TODO validate inputs
        if email and password:
            if authenticate_user(email, password):
                id = get_user_id(email, password)
                user = User(id)
                login_user(user)
                return redirect(url_for('.dashboard'))
            # TODO else
    return redirect("/")

@app.route('/signout', methods=["POST", "GET"])
@login_required
def signout():
    if request.method=="POST":
        logout_user()
        return redirect("/")
    return redirect("/")


@app.route('/dashboard', methods=["POST", "GET"])
@login_required
def dashboard(user=''):
    print('*******  {}  ********'.format(inspect.stack()[0][3]))
    if request.method=="POST":
        form = request.form

    if request.method=="GET":
        id = current_user.id
        user = get_user_by_id(id)

    return render_template("dashboard.html", user=user)

@app.route('/change_password', methods=["POST", "GET"])
@login_required
def change_password():
    print('*******  {}  ********'.format(inspect.stack()[0][3]))
    if request.method=="POST":
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

# @app.route('/admin/newElec', methods=["POST", "GET"])
# def admin_newElec():
#     if request.method == "POST":
#         elec_id = request.form["elec_id"]
#         elec_type = request.form["elec_type"]
#         start_date = request.form["start_date"]
#         finish_date = request.form["finish_date"]
#         vote_count = request.form["vote_count"]
#         make_new_elec(elec_id, elec_type, start_date, finish_date, vote_count)
#     return render_template("admin_newelec.html")
#
#
# @app.route('/user/vote', methods=["POST", "GET"])
# def vote():
#     if request.method == "POST":
#         nomin_id = request.form["nomin_id"]
#         voter_id = request.form["voter_id"]
#         vote(nomin_id, voter_id)
#     return render_template("")
#
#
# ##############################################################################################################
#
#
# @app.route('/Admin/AddElections', methods=["POST", "GET"])
# def AddElections(error = '', elecsYear = []):
#     now = jdatetime.datetime.today().year
#     for year in range(now,now + 10):
#         elecsYear.append(year)
#     if request.method == "POST":
#         try:
#             start_date_day = request.form["start_date_day"]
#             start_date_month = request.form["start_date_month"]
#             start_date_year = request.form["finish_date_year"]
#             finish_date_day = request.form["finish_date_day"]
#             finish_date_month = request.form["finish_date_month"]
#             finish_date_year = request.form["finish_date_year"]
#             print(start_date_day)
#             start_date = '{}-{}-{}'.format(start_date_year,start_date_month,start_date_day)
#             finish_date = '{}-{}-{}'.format(finish_date_year,finish_date_month,finish_date_day)
#             error =  make_new_elec(start_date, finish_date)
#         except:
#             error = 'ورودی نامعتبر!'
#     return render_template("Admin/AddElections.html", error = error, elecsYear = elecsYear)
#
#
#
#
#
#
#
# @app.route('/Admin/AddNomin', methods=["POST", "GET"])
# def AddNomin(error = '', nominBirthYears = [], elecsYear = get_editable_elecs()):
#     now = jdatetime.datetime.today().year
#     for year in range(now - 18,now - 68,-1):
#         nominBirthYears.append(year)
#     if request.method == "POST":
#             try:
#                 nomin_nid = request.form["nomin_nid"]
#                 nomin_name = request.form["nomin_name"]
#                 nomin_gender = request.form["nomin_gender"]
#                 # print nomin_name
#                 nomin_birthdate_day = request.form["nomin_birthdate_day"]
#                 nomin_birthdate_month = request.form["nomin_birthdate_month"]
#                 nomin_birthdate_year = request.form["nomin_birthdate_year"]
#                 print(nomin_birthdate_day)
#                 nomin_party = request.form["nomin_party"]
#                 # print nomin_party
#                 elec_year = request.form["elec_year"]
#                 nomin_birthdate = '{}-{}-{}'.format(nomin_birthdate_day,nomin_birthdate_month,nomin_birthdate_year)
#                 # print '{},{},{},{},{},{}'.format(nomin_nid, nomin_name, nomin_gender, nomin_birthdate, nomin_party, elec_year)
#                 add_nominate(nomin_nid, nomin_name, nomin_gender, nomin_birthdate, nomin_party, elec_year)
#             except:
#                 error =  'ورودی نامعتبر!'
#
#     return render_template('/Admin/AddNomin.html', error = error, nominBirthYears = nominBirthYears, elecsYear = elecsYear)
#
#
#
#
#
# @app.route('/Admin/AddAdmin', methods=["POST", "GET"])
# def AddAdmin():
#     # TODO
#     return render_template ('/Admin/AddAdmin.html')
#
#
# @app.route('/Admin/cdResult', methods=["POST", "GET"])
# def cdResult():
#     # TODO
#     return render_template ('/Admin/cdResult.html')
#
#
#
# @app.route('/Admin/ppResult', methods=["POST", "GET"])
# def ppResult():
#     # TODO
#     return render_template ('/Admin/ppResult.html')
#
#
# @app.route('/Admin/Login', methods=["POST", "GET"])
# def Login():
#     # TODO
#     return render_template ('/Admin/Login.html')
#
#
#


if __name__ == "__main__":
    app.run(port=8082, debug=True)
