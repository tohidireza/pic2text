from __future__ import unicode_literals
import sqlite3
import os
import jdatetime
# -*- coding: utf-8 -*-
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

db_name = os.path.join(PROJECT_ROOT, 'online_voting_system')

# setting

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Admin (
                      admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username NVARCHAR(200) NOT NULL UNIQUE,
                      password NVARCHAR(50)
    ); ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Election (
                      elec_id INTEGER PRIMARY KEY,
                      start_date DATE,
                      finish_date DATE
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Nominate (
                      nomin_id INTEGER PRIMARY KEY ,
                      nomin_nid  NVARCHAR(20) ,
                      nomin_name NVARCHAR(200),
                      nomin_gender INTEGER ,
                      nomin_birthdate DATE,
                      nomin_party NVARCHAR(200),
                      elec_id  INTEGER,
                      FOREIGN KEY (elec_id) REFERENCES Election(elec_id)

    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Voter (
                      voter_id INTEGER PRIMARY KEY ,
                      voter_nid NVARCHAR(20) ,
                      voter_name NVARCHAR(200),
                      voter_gender INTEGER,
                      voter_birthdate DATE,
                      voter_country NVARCHAR(200),
                      voter_province NVARCHAR(200),
                      voter_city NVARCHAR(200)
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Vote (
                      nomin_id INTEGER,
                      voter_id INTEGER,
                      elec_id  INTEGER,
                      PRIMARY KEY (nomin_id, voter_id),
                      FOREIGN KEY (nomin_id) REFERENCES Nominate(nomin_id),
                      FOREIGN KEY (elec_id) REFERENCES Election(elec_id),
                      FOREIGN KEY (voter_id) REFERENCES Voter(voter_id)
    );''')

    conn.close()


def make_new_elec(start_date, finish_date):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    splitedStartDate = start_date.split('-')
    elec_id = int(splitedStartDate[0])
    nowDate = str(jdatetime.datetime.today()).split(' ')[0]
    cursor.execute(" SELECT julianday('{}') - julianday('{}') ".format(nowDate,start_date))
    startDiff = (cursor.fetchall())[0][0]
    cursor.execute(" SELECT julianday('{}') - julianday('{}')".format(finish_date, start_date))
    datediff = cursor.fetchall()[0][0]
    if datediff > 0 and startDiff < 0:
        cursor.execute(" INSERT INTO Election (elec_id,start_date,finish_date) \
                        VALUES ({},'{}','{}') ".format(elec_id, start_date, finish_date))
    else:
        return 'invalid input!'

    conn.commit()
    conn.close()
    return ''


def add_nominate(nomin_nid, nomin_name, nomin_gender, nomin_birthdate, nomin_party, elec_year):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    nomin_id = int(str(elec_year) + str(nomin_nid))
    cursor.execute(" INSERT INTO Nominate (nomin_id, nomin_nid, nomin_name, nomin_gender ,nomin_birthdate ,nomin_party, elec_id) \
                    VALUES ({},'{}','{}',{},'{}','{}',{}) ".format(nomin_id, nomin_nid, nomin_name, nomin_gender,
                                                                   nomin_birthdate, nomin_party, elec_year))

    conn.commit()
    conn.close()


def check_voter_vote_count(voter_id, elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(Vote.voter_id) FROM Vote \
                    WHERE voter_id = ? AND elec_id = ? ", (voter_id, elec_id))
    vote_count = cursor.fetchall()[0][0]
    conn.commit()
    conn.close()
    return vote_count


def check_vote_date_valid(elec_year):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    nowDate = str(jdatetime.datetime.today()).split(' ')[0]
    cursor.execute("SELECT julianday('{}') - julianday(start_date) FROM \
                    Election WHERE elec_id = {}".format(nowDate,elec_year))
    startDiff = cursor.fetchall()[0][0]
    if startDiff >= 0:
        cursor.execute("SELECT julianday('{}') - julianday(finish_date) FROM \
                         Election WHERE elec_id = {}".format(nowDate,elec_year))
        finishDiff = cursor.fetchall()[0][0]
        if finishDiff <= 0:
            conn.commit()
            conn.close()
            return 1

    conn.commit()
    conn.close()
    return 0


def check_vote_age_valid(voter_birthdate):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    nowDate = str(jdatetime.datetime.today()).split(' ')[0]
    cursor.execute("SELECT julianday('{}') - julianday('{}')".format(nowDate,voter_birthdate, ))
    voter_age = cursor.fetchall()[0][0] / 365
    conn.commit()
    conn.close()
    if voter_age >= 18:
        return 1

    return 0


def add_voter_and_vote(voter_nid, voter_name, voter_gender, voter_birthdate, voter_country, voter_province, voter_city
                       , nomin_id, elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    voter_id = int(str(elec_id) + str(voter_nid))
    if check_voter_vote_count(voter_id, elec_id) == 1:
        # TODO voted_error
        print('voted_error')
        pass
    elif check_vote_date_valid(elec_id) == 0:
        # TODO date_error
        print('date_error')
        pass
    elif check_vote_age_valid(voter_birthdate) == 0:
        # TODO age_error
        print('age_error')
        pass
    else:
        cursor.execute(" INSERT INTO Voter (voter_id, voter_nid, voter_name, voter_gender, voter_birthdate, voter_country, voter_province, voter_city) \
                          VALUES ('{}','{}','{}',{},'{}','{}','{}','{}') ".format(voter_id, voter_nid, voter_name,
                                                                                  voter_gender, voter_birthdate,
                                                                                  voter_country, voter_province,
                                                                                  voter_city))

        cursor.execute(" INSERT INTO Vote (nomin_id, voter_id, elec_id) \
                         VALUES ('{}','{}','{}') ".format(nomin_id, voter_id, elec_id))
    conn.commit()
    conn.close()


def get_nomin_vote_count_in_a_year(nomin_name, elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(Vote.voter_id) FROM Voter\
                    INNER JOIN Vote\
                    ON Voter.voter_id = Vote.voter_id AND Vote.elec_id = ?\
                    INNER JOIN Nominate\
                    ON Nominate.nomin_id = Vote.nomin_id AND nomin_name = ? ", (elec_id, nomin_name))
    vote_count = cursor.fetchall()[0][0]
    conn.commit()
    conn.close()
    return vote_count


def get_party_vote_count_in_a_year(nomin_party, elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(Vote.voter_id) FROM Voter\
                    INNER JOIN Vote\
                    ON Voter.voter_id = Vote.voter_id AND Vote.elec_id = ?\
                    INNER JOIN Nominate\
                    ON Nominate.nomin_id = Vote.nomin_id AND nomin_party = ? ", (elec_id, nomin_party))
    vote_count = cursor.fetchall()[0][0]
    conn.commit()
    conn.close()
    return vote_count


def get_nomin_vote_count_in_a_year_in_each_province(nomin_name, elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT voter_province, COUNT(Vote.voter_id) FROM Voter\
                    INNER JOIN Vote\
                    ON Vote.voter_id = Voter.voter_id\
                    INNER JOIN Nominate\
                    ON Nominate.nomin_id = Vote.nomin_id AND Vote.elec_id = ? AND nomin_name = ?\
                    GROUP BY voter_province ", (elec_id, nomin_name))
    vote_province_and_count = cursor.fetchall()
    conn.commit()
    conn.close()
    return vote_province_and_count  # TODO split array elements


def get_nomin_vote_count_in_a_year_in_each_city(nomin_name, elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT voter_province, COUNT(Vote.voter_id) FROM Voter\
                    INNER JOIN Vote\
                    ON Vote.voter_id = Voter.voter_id\
                    INNER JOIN Nominate\
                    ON Nominate.nomin_id = Vote.nomin_id AND Vote.elec_id = ? AND nomin_name = ?\
                    GROUP BY voter_city ", (elec_id, nomin_name))
    vote_city_and_count = cursor.fetchall()
    conn.commit()
    conn.close()
    return vote_city_and_count  # TODO split array elements


def get_party_vote_count_in_a_year_in_each_province(nomin_party, elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT voter_province, COUNT(Vote.voter_id) FROM Voter\
                    INNER JOIN Vote\
                    ON Vote.voter_id = Voter.voter_id\
                    INNER JOIN Nominate\
                    ON Nominate.nomin_id = Vote.nomin_id AND Vote.elec_id = ? AND nomin_party = ?\
                    GROUP BY voter_province ", (elec_id, nomin_party))
    vote_province_and_count = cursor.fetchall()
    conn.commit()
    conn.close()
    return vote_province_and_count  # TODO split array elements


def get_party_vote_count_in_a_year_in_each_city(nomin_party, elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT voter_city, COUNT(Vote.voter_id) FROM Voter\
                    INNER JOIN Vote\
                    ON Vote.voter_id = Voter.voter_id\
                    INNER JOIN Nominate\
                    ON Nominate.nomin_id = Vote.nomin_id AND Vote.elec_id = ? AND nomin_party = ?\
                    GROUP BY voter_city ", (elec_id, nomin_party))
    vote_city_and_count = cursor.fetchall()
    conn.commit()
    conn.close()
    return vote_city_and_count  # TODO split array elements


def get_nomin_vote_count_in_each_year(nomin_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT elec_id, COUNT(Vote.voter_id) FROM Nominate\
                    INNER JOIN Vote\
                    ON Vote.nomin_id = Nominate.nomin_id AND nomin_name = ?\
                    GROUP BY elec_id", (nomin_name,))
    vote_year_and_count = cursor.fetchall()
    conn.commit()
    conn.close()
    return vote_year_and_count  # TODO split array elements


def get_party_vote_count_in_each_year(nomin_party):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT elec_id, COUNT(Vote.voter_id) FROM Nominate\
                    INNER JOIN Vote\
                    ON Vote.nomin_id = Nominate.nomin_id AND nomin_party = ?\
                    GROUP BY elec_id", (nomin_party,))
    vote_year_and_count = cursor.fetchall()
    conn.commit()
    conn.close()
    return vote_year_and_count  # TODO split array elements


def get_each_nomin_vote_count_in_a_year(elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT nomin_name, COUNT(Vote.voter_id) FROM Nominate\
                    INNER JOIN Vote\
                    ON Vote.nomin_id = Nominate.nomin_id AND Vote.elec_id = ?\
                    GROUP BY nomin_name", (elec_id,))
    vote_nomin_and_count = cursor.fetchall()
    conn.commit()
    conn.close()
    return vote_nomin_and_count  # TODO split array elements


def get_each_party_vote_count_in_a_year(elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT nomin_party, COUNT(Vote.voter_id) FROM Nominate\
                    INNER JOIN Vote\
                    ON Vote.nomin_id = Nominate.nomin_id AND Vote.elec_id = ?\
                    GROUP BY nomin_party", (elec_id,))
    vote_party_and_count = cursor.fetchall()
    conn.commit()
    conn.close()
    return vote_party_and_count  # TODO split array elements


def get_vote_count_in_a_year(elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(voter_id) FROM Vote\
                    WHERE elec_id = ?", (elec_id,))
    vote_count = cursor.fetchall()[0][0]
    conn.commit()
    conn.close()
    return vote_count


def get_showable_elecs():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    nowDate = str(jdatetime.datetime.today()).split(' ')[0]
    cursor.execute("SELECT elec_id FROM \
                    Election WHERE (julianday('{}') - julianday(start_date) >= 0)".format(nowDate,))
    fetch = cursor.fetchall()
    showable_elecs = []
    for row in fetch:
        showable_elecs.append(row[0])
    conn.commit()
    conn.close()
    return showable_elecs


def get_editable_elecs():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    nowDate = str(jdatetime.datetime.today()).split(' ')[0]
    cursor.execute("SELECT elec_id FROM \
                    Election WHERE (julianday('{}') - julianday(start_date) < 0)".format(nowDate,))
    fetch = cursor.fetchall()
    editable_elecs = []
    for row in fetch:
        editable_elecs.append(row[0])
    conn.commit()
    conn.close()
    return editable_elecs


# def get_recent_elec():
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute("SELECT MAX(elec_id) FROM Election")
#     recent_elec = cursor.fetchall()[0][0]
#     print(recent_elec)
#     conn.commit()
#     conn.close()
#     if check_valid_elec(recent_elec):
#         return recent_elec
#     else:
#         # TODO invalid_elec
#         pass


def get_elecs_year():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT elec_id FROM Election")
    fetch = cursor.fetchall()
    conn.commit()
    conn.close()
    elecs_year = []
    for row in fetch:
        elecs_year.append(row[0])
    return elecs_year  # TODO split array elements


def get_nomins_information(elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT nomin_id, nomin_name, nomin_party FROM Nominate \
                    WHERE elec_id = {}".format(elec_id, ))
    nomins_information = cursor.fetchall()
    conn.commit()
    conn.close()
    return nomins_information  # TODO split array


def get_nomins_name(elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT nomin_name FROM Nominate \
                    WHERE elec_id = {}".format(elec_id, ))
    fetch = cursor.fetchall()
    conn.commit()
    conn.close()
    nomins_name = []
    for row in fetch:
        nomins_name.append(row[0])
    return nomins_name  # TODO split array


def get_nomins_party(elec_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT nomin_party FROM Nominate \
                    WHERE elec_id = {}".format(elec_id, ))
    nomins_party = cursor.fetchall()
    conn.commit()
    conn.close()
    return nomins_party  # TODO split array
