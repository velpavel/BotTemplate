# -*- coding: utf-8 -*-
import sqlite3
import configparser
import datetime

config = configparser.ConfigParser()
config.read('config.ini')

SQLITEDB = config['DB']['Dbfile']

def sql_lite_connect():
    db= sqlite3.connect(SQLITEDB)
    cursor = db.cursor()
    return (db, cursor)

def sql_lite_close(db, commit=True):
    if commit: db.commit()
    db.close()

def get_user_operation(id):
    sql = '''select Telegramid, current_operation, operation_status, additional_info from user_operation where Telegramid=?'''
    (db, cursor) = sql_lite_connect()
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT into user_operation (Telegramid) values (?)', (id,))
        operation = (None, None, None)
    else:
        operation = (result[1], result[2], result[3])
    sql_lite_close(db)
    return operation

def put_user_operation(id, operation=None, status=0, additional_info=None):
    sql_insert = '''insert or replace into user_operation (Telegramid, current_operation, operation_status, additional_info) values (?,?,?,?)'''
    (db, cursor) = sql_lite_connect()
    cursor.execute(sql_insert, (id, operation, status, additional_info))
    sql_lite_close(db)

def is_user_registered(id):
    sql = '''select Telegramid from users where Telegramid=? and RegistrationDone=1'''
    (db, cursor) = sql_lite_connect()
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    sql_lite_close(db)
    return True if len(result)>0 else False

def add_new_user(id):
    sql = 'insert into users (Telegramid) values(?)'
    (db, cursor) = sql_lite_connect()
    cursor.execute(sql, (id,))
    sql_lite_close(db)

def is_user_exist(id):
    sql = '''select Telegramid from users where Telegramid=?'''
    (db, cursor) = sql_lite_connect()
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    sql_lite_close(db)
    return True if len(result) > 0 else False

def register_user(id, phone=None, name=None, region=None, email=None, registrationDone=0):
    if not is_user_exist(id):
        add_new_user(id)
    parameters=[]
    sql='''update users set'''
    sql_middle='where Telegramid=?'
    if phone: sql+=' Phone=?,'; parameters.append(phone);
    if name: sql+=' Name=?,'; parameters.append(name);
    if region: sql+=' Region=?,'; parameters.append(region);
    if email: sql += ' Email=?,'; parameters.append(email);
    if registrationDone:
        sql+=' RegistrationDone=?, RegistrationDate=?,'
        parameters.append(registrationDone)
        parameters.append(datetime.datetime.now().strftime('%Y-%m-%d %X'))
    sql=sql[:-1]+sql_middle
    parameters.append(id)
    (db, cursor) = sql_lite_connect()
    cursor.execute(sql, parameters)
    sql_lite_close(db)

