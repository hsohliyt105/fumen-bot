# -*- coding: utf-8 -*-

from os import getenv
from typing import Literal

from discord import User
from pymysql import connect, cursors
from dotenv import load_dotenv

load_dotenv(encoding="UTF-8")
MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")

def save_user(user: User, auto: bool = True, duration: float = 0.5, transparency: bool = True, background: str = "", theme: Literal["light", "dark"] = "dark", comment: bool = True):
    conn = connect(host="localhost", user="root", db="fumen_bot", password=MYSQL_PASSWORD, charset="utf8", cursorclass=cursors.DictCursor)
    cur = conn.cursor()

    try:
        sql = f"INSERT INTO users(user_id, auto, duration, transparency, background, theme, comment) VALUES({user.id}, {auto}, {duration}, {transparency}, '{background}', '{theme}', {comment})"
        cur.execute(sql)
        conn.commit()

    except:
        sql = f"UPDATE users SET auto='{auto}', duration='{duration}', transparency='{transparency}', background='{background}', theme='{theme}', comment='{comment}' WHERE discord_id={user.id}"
        cur.execute(sql)
        conn.commit()

    conn.close()

    return

def load_user(user: User):
    conn = connect(host="localhost", user="root", db="fumen_bot", password=MYSQL_PASSWORD, charset="utf8", cursorclass=cursors.DictCursor)
    cur = conn.cursor()

    sql = f"SELECT * FROM users WHERE user_id={user.id}"
    cur.execute(sql) 
    result = cur.fetchall()
    conn.close()

    if len(result) == 0:
        return

    return result[0]

def delete_user(user: User):
    conn = connect(host="localhost", user="root", db="fumen_bot", password=MYSQL_PASSWORD, charset="utf8", cursorclass=cursors.DictCursor)
    cur = conn.cursor()

    sql = f"DELETE FROM users WHERE user_id={user.id}"
    cur.execute(sql) 
    
    conn.commit()
    conn.close()

    return