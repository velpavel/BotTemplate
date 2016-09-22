# -*- coding: utf-8 -*-
import sqlite3, inspect
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

def last_users():
    sql_count = 'select count(*) from users'
    sql_last_10='select Name, RegistrationDate from users order by RegistrationDate Desc Limit 10'
    (db, cursor) = sql_lite_connect()
    cursor.execute(sql_count)
    result = cursor.fetchone()
    count=result[0]
    cursor.execute(sql_last_10)
    result = cursor.fetchall()
    last=[]
    for entr in result:
        last.append('{}. {}'.format(entr[0], entr[1]))
    sql_lite_close(db)
    return (count, last)

def save_to_log(from_who='user', message=None, comment_text='', msg_text=''):
    sql = '''insert into log (datetime, from_who, user_id, msg_text, operation, status, additional_info, function, comment)
                values (?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    if from_who not in ('bot', 'user'): comment_text += ' '+from_who; from_who='need_help'
    (operation, status, additional_info) = (None, None, None)
    id = None
    if message:
        id = message.from_user.id
        if from_who == 'user':
            if message.content_type == 'text':
                msg_text = message.text
            if message.content_type == 'contact':
                msg_text = str(message.contact)
        (operation, status, additional_info) = get_user_operation(message.from_user.id)
    (db, cursor) = sql_lite_connect()
    cursor.execute(sql, (datetime.datetime.now().strftime('%Y-%m-%d %X'), from_who, id, msg_text,
                         operation, status, additional_info,
                         inspect.stack()[1][3], comment_text))
    sql_lite_close(db)

def last_log_rec(last=10):
    sql='select * from log order by datetime Desc Limit ?'
    (db, cursor) = sql_lite_connect()
    cursor.execute(sql,(last,))
    result = cursor.fetchall()
    sql_lite_close(db)
    return 'Последние записи из лога. Количество {}:\n'.format(last)+'\n'.join([' | '.join([str(a) for a in entry]) for entry in result])
