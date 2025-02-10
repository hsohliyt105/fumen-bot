# -*- coding: utf-8 -*-

from os import environ
from typing import Literal

from pymysql import connect, cursors
from dotenv import load_dotenv

load_dotenv(encoding="UTF-8")

HOST = "localhost"
USER = "root"
PASSWORD = environ['MYSQL_PASSWORD']
CHARSET = "utf8"
CURSORCLASS = cursors.DictCursor
DB = "fumen_bot"

class User():
    id = 123

def save_user(user: User, options: dict):
    prev_options = load_user(user)

    conn = connect(host=HOST, user=USER, db=DB, password=PASSWORD, charset=CHARSET, cursorclass=CURSORCLASS)
    cur = conn.cursor()

    if prev_options is not None:
        for option_name in options:
            if options[option_name] is None:
                options[option_name] = prev_options[option_name]
        sql = f"UPDATE users SET auto=%s, duration=%s, transparency=%s, background=%s, theme=%s, comment=%s WHERE user_id=%s"
        cur.execute(sql, (options['auto'], options['duration'], options['transparency'], options['background'], options['theme'], options['comment'], user.id))
        conn.commit()

    else:
        sql = f"INSERT INTO users(user_id, auto, duration, transparency, background, theme, comment) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(sql, (user.id, options['auto'], options['duration'], options['transparency'], options['background'], options['theme'], options['comment']))
        conn.commit()

    conn.close()

    return
    
def load_user(user: User):
    conn = connect(host=HOST, user=USER, db=DB, password=PASSWORD, charset=CHARSET, cursorclass=CURSORCLASS)
    cur = conn.cursor()

    sql = f"SELECT * FROM users WHERE user_id={user.id}"
    cur.execute(sql) 
    result = cur.fetchall()
    conn.close()

    if len(result) == 0:
        return

    return result[0]

def delete_user(user: User):
    conn = connect(host=HOST, user=USER, db=DB, password=PASSWORD, charset=CHARSET, cursorclass=CURSORCLASS)
    cur = conn.cursor()

    sql = f"DELETE FROM users WHERE user_id=%s"
    cur.execute(sql, (user.id)) 
    
    conn.commit()
    conn.close()

    return

options = {
            'auto': None,
            'duration': None,
            'transparency': None,
            'background': None,
            'theme': None,
            'comment': None
        }
user = User()
options['auto'] = True
save_user(user, options)
print(load_user(user))
options['auto'] = None
options['duration'] = 1.2
save_user(user, options)
print(load_user(user))