# -*- coding: utf-8 -*-

from os import getenv
from typing import Literal

from pymysql import connect, cursors
from dotenv import load_dotenv

load_dotenv(encoding="UTF-8")
MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")

def save_user(user, auto: bool = True, duration: float = 0.5, transparency: bool = True, background: str = None, theme: Literal["light", "dark"] = "dark", comment: bool = True):
    conn = connect(host="localhost", user="root", db="fumen_bot", password=MYSQL_PASSWORD, charset="utf8", cursorclass=cursors.DictCursor)
    cur = conn.cursor()

    try:
        sql = f"INSERT INTO users(user_id, auto, duration, transparency, background, theme, comment) VALUES({user.id}, '{edu_code}', '{school_code}', '{school_name}')"
        cur.execute(sql)
        conn.commit()

    except:
        sql = f"UPDATE users SET edu_code='{edu_code}', school_code='{school_code}', school_name='{school_name}' WHERE discord_id={user.id}"
        cur.execute(sql)
        conn.commit()

    conn.close()

    return

def save_subscription(user, subscribe_hour, subscribe_min):
    conn = connect(host="localhost", user="root", db="school_food_bot", password=MYSQL_PASSWORD, charset="utf8", cursorclass=cursors.DictCursor)
    cur = conn.cursor()

    sql = f"UPDATE users SET subscribe_hour='{subscribe_hour}' subscribe_min='{subscribe_min}' WHERE discord_id={user.id}"
    cur.execute(sql)
    conn.commit()
    return 

def load_user(discord_id):
    conn = connect(host="localhost", user="root", db="school_food_bot", password=MYSQL_PASSWORD, charset="utf8", cursorclass=cursors.DictCursor)
    cur = conn.cursor()

    sql = f"SELECT * FROM users WHERE discord_id={discord_id}"
    cur.execute(sql) 
    result = cur.fetchall()
    conn.close()

    if len(result) == 0:
        return

    return result[0]

def delete_user(discord_id):
    conn = connect(host="localhost", user="root", db="school_food_bot", password=MYSQL_PASSWORD, charset="utf8", cursorclass=cursors.DictCursor)
    cur = conn.cursor()

    sql = f"DELETE FROM users WHERE discord_id={discord_id}"
    cur.execute(sql) 
    
    conn.commit()
    conn.close()

    return