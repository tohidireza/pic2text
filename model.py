from __future__ import unicode_literals
import sqlite3
import os
import hashlib

# -*- coding: utf-8 -*-
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

db_name = os.path.join(PROJECT_ROOT, 'pic2text_db')


# setting

def create_database():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name text NOT NULL,
                      last_name text NOT NULL,
                      email text NOT NULL UNIQUE,
                      password text,
                      is_deleted varchar(1) not NULL  DEFAULT '0'
                    ); ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS History (
                      hist_id INTEGER PRIMARY KEY,
                      user_id INTEGER,
                      file_name text NOT NULL,
                      file_type text NOT NULL,
                      status text NOT NULL,
                      src_file text NOT NULL UNIQUE,
                      dst_file text NOT NULL UNIQUE,
                      is_deleted varchar(1) not NULL  DEFAULT '0',
                      FOREIGN KEY (user_id) REFERENCES Users(user_id)
                    );''')
    conn.close()


def hash_pass(password):
    salt = "salt :D"
    password = password + salt
    hashed = hashlib.md5(password.encode())
    return hashed.hexdigest()


def add_user(first_name, last_name, email, password):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    password = hash_pass(password)
    cursor.execute(" INSERT INTO Users (first_name, last_name, email, password) \
                    VALUES ('{}','{}','{}','{}') ".format(first_name, last_name, email, password))
    conn.commit()
    conn.close()


def check_email_uniqueness(email):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("select * from Users where \
                        email='%s' and is_deleted=0 ;" % \
                   (email))

    user = cursor.fetchall()

    if len(user) != 0:
        return False

    return True


def authenticate_user(email, password):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("select * from Users where \
                        email='%s' and password='%s' and is_deleted=0 ;" % \
                   (email, hash_pass(password)))

    user = cursor.fetchall()
    return len(user) != 0


def authenticate_user_by_id(id, password):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("select * from Users where \
                        user_id='%s' and password='%s' and is_deleted=0 ;" % \
                   (id, hash_pass(password)))

    user = cursor.fetchall()
    return len(user) != 0


def get_user_id(email, password):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("select user_id from Users where \
                        email='%s' and password='%s' and is_deleted=0 ;" % \
                   (email, hash_pass(password)))

    user_id = cursor.fetchall()[0][0]
    return user_id


def get_user_by_id(id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("select first_name,last_name,email from Users where \
                        user_id='%s' and is_deleted=0 ;" % \
                   (id))

    user = cursor.fetchall()[0]
    return dict(zip(['first_name', 'last_name', 'email'], user))


def change_user_password(id, newPassword):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("update Users \
                        set password = '%s' \
                         where user_id = '%s';" % \
                   (hash_pass(newPassword), id))

    conn.commit()
    conn.close()


def add_record(user_id, file_name, file_type, src_file, dst_file):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(" INSERT INTO History (user_id, file_name, file_type, src_file, dst_file, status) \
                    VALUES ('{}','{}','{}','{}','{}','{}') ".format(user_id, file_name, file_type, src_file, dst_file,'پردازش و تبدیل موفق'))
    conn.commit()
    conn.close()
