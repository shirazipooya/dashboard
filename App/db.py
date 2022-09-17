import os
import sys
import itertools
import psycopg2
from sqlalchemy import *

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

POSTGRES_USER_NAME = 'postgres'
POSTGRES_PASSWORD = '1234'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'

MY_DB_LIST = [ "data", "layers"]
MY_DB_POSTGIS_LIST = ["layers"]

conn = psycopg2.connect(
    database="postgres",
    user=POSTGRES_USER_NAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

conn.autocommit = True

cursor = conn.cursor()

sql = '''SELECT datname FROM pg_catalog.pg_database;'''

cursor.execute(sql)

db_list_exist = list(itertools.chain.from_iterable(cursor.fetchall()))



for i in MY_DB_LIST:
    if i not in db_list_exist:
        sql = f"CREATE DATABASE {i}"
        cursor.execute(sql)
        if i in MY_DB_POSTGIS_LIST:
            conn_new = psycopg2.connect(
                database=i,
                user=POSTGRES_USER_NAME,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT
            )
            conn_new.autocommit = True
            cursor = conn_new.cursor()
            sql = "CREATE EXTENSION postgis;"
            cursor.execute(sql)
            conn_new.close()            

conn.close()