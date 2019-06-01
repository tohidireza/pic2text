# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, render_template
from flask import redirect
from flask import request
from flask import url_for
from model import *
import jdatetime



app = Flask(__name__)
error = ''
# bootstrap = Bootstrap(app)

@app.route('/', methods=["POST", "GET"])
def index():
    return render_template("index.html")

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
