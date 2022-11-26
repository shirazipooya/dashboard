import os
import sys
import itertools
import psycopg2
from sqlalchemy import *
import redis

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

POSTGRES_USER_NAME = 'postgres'
POSTGRES_PASSWORD = '1234'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'

MY_DB_LIST = [ "data", "layers"]
MY_DB_POSTGIS_LIST = ["layers"]


def create_database():
    
    global POSTGRES_USER_NAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, MY_DB_LIST, MY_DB_POSTGIS_LIST
    
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
    
    return None

create_database()


# -----------------------------------------------------------------------------
# DATABASE CONNECTION: data
# -----------------------------------------------------------------------------
# DB:
POSTGRES_DB_DATA = "data"
DB_DATA = f"postgresql://{POSTGRES_USER_NAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_DATA}"
ENGINE_DATA = create_engine(DB_DATA, echo=False)

# TABLES:
DB_DATA_TABLE_GEOINFO = "geoinfo"
DB_DATA_TABLE_RAWDATA = "raw_data"
DB_DATA_TABLE_RAW_DATA_DELETED = "raw_data_deleted"
DB_DATA_TABLE_RAW_DATA_MODIFIED = "raw_data_modified"
DB_DATA_TABLE_MODIFIEDDATA = "modified_data"
DB_DATA_TABLE_INTERPOLATEDDATA = "interpolated_data"
DB_DATA_TABLE_SYNCDATEDATA = "syncdate_data"
DB_DATA_TABLE_DATA = "data"
DB_DATA_TABLE_HYDROGRAPH = "hydrograph"
DB_DATA_TABLE_TEMPORARY = "temporary"


# -----------------------------------------------------------------------------
# DATABASE CONNECTION: layers
# -----------------------------------------------------------------------------
# DB:
POSTGRES_DB_LAYERS = "layers"
DB_LAYERS = f"postgresql://{POSTGRES_USER_NAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_LAYERS}"
ENGINE_LAYERS = create_engine(DB_LAYERS, echo=False)

# TABLES:
DB_LAYERS_TABLE_WELL = "well"
DB_LAYERS_TABLE_AQUIFER = "aquifer"
DB_LAYERS_TABLE_MAHDOUDE = "mahdoude"
DB_LAYERS_TABLE_THIESSEN = "thiessen"
DB_LAYERS_TABLE_TEMPORARY= "temporary"



# -----------------------------------------------------------------------------
# DATABASE CONNECTION: layers
# -----------------------------------------------------------------------------
REDIS_DB = redis.Redis(host='localhost', port=6379, db=0)