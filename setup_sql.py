# -*- coding: utf-8 -*-

from os import environ

from pymysql import connect, cursors
from pymysql.constants import CLIENT
from dotenv import load_dotenv

load_dotenv(encoding="UTF-8")

HOST = "localhost"
USER = "root"
PASSWORD = environ['MYSQL_PASSWORD']
CHARSET = "utf8"
CURSORCLASS = cursors.DictCursor

conn = connect(host=HOST, user=USER, password=PASSWORD, charset=CHARSET, cursorclass=CURSORCLASS, client_flag=CLIENT.MULTI_STATEMENTS)
cur = conn.cursor()

sql = f"""
CREATE DATABASE fumen_bot;
USE fumen_bot;
CREATE TABLE `fumen_bot`.`users` (
  `user_id` INT NOT NULL,
  `theme` VARCHAR(10) NULL,
  `auto` TINYINT NULL,
  `duration` FLOAT NULL,
  `transparency` TINYINT NULL,
  `background` VARCHAR(10) NULL,
  `comment` TINYINT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE);
"""

cur.execute(sql)
conn.commit()

conn.close()