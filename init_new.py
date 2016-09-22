import sqlite3
import configparser
import shutil, os

if not os.path.exists(r'config.ini'):
    shutil.copy(r'config_skeleton.ini', r'config.ini')

config = configparser.ConfigParser()
config.read('config.ini')
SQLITEDB = config['DB']['Dbfile']

sql = '''PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: users
DROP TABLE IF EXISTS users;
CREATE TABLE users (Telegramid INTEGER PRIMARY KEY NOT NULL, Phone INTEGER, Name VARCHAR (50), Email VARCHAR (50), RegistrationDone BOOLEAN DEFAULT (0) NOT NULL, RegistrationDate DATETIME);

-- Таблица: user_operation
DROP TABLE IF EXISTS user_operation;
CREATE TABLE user_operation (Telegramid INTEGER UNIQUE NOT NULL PRIMARY KEY, current_operation TEXT, operation_status, additional_info TEXT);

-- Индекс: idx_user_operation_telegramid
DROP INDEX IF EXISTS idx_user_operation_telegramid;
CREATE UNIQUE INDEX idx_user_operation_telegramid ON user_operation (Telegramid);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;'''

if not os.path.exists(SQLITEDB):
    con = sqlite3.connect(SQLITEDB)
    cur = con.cursor()
    cur.executescript(sql)
    con.commit()
    con.close()