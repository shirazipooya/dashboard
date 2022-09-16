import itertools
import numpy as np
import pandas as pd
import sqlalchemy as sa
import psycopg2
import plotly.graph_objects as go
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from App.db import POSTGRES_USER_NAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


# -----------------------------------------------------------------------------
# CONSTANT VARIABLES
# -----------------------------------------------------------------------------
NO_MATCHING_GRAPH_FOUND = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No Graph Found ...",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 36}
            }
        ]
    }
}

# -----------------------------------------------------------------------------
# BASE MAP
# -----------------------------------------------------------------------------
BASE_MAP = go.Figure(
    go.Scattermapbox(
        
    )
)

BASE_MAP.update_layout(
    mapbox={
        'style': "stamen-terrain",
        'center': {
            'lon': 59.55,
            'lat': 36.25
        },
        'zoom': 5.5
    },
    showlegend=False,
    hovermode='closest',
    margin={'l':0, 'r':0, 'b':0, 't':0},
    autosize=False
)


# -----------------------------------------------------------------------------
# DATABASE CONNECTION: data
# -----------------------------------------------------------------------------
POSTGRES_DB_NAME = "data"
TABLE_NAME_GEOINFO = "geoinfo"
TABLE_NAME_RAW_DATA = "raw_data"
TABLE_NAME_MODIFIED_DATA = "modified_data"
TABLE_NAME_INTERPOLATED_DATA = "interpolated_data"
TABLE_NAME_SYNCDATE_DATA = "syncdate_data"
TABLE_NAME_DATA = "data"

db = f"postgresql://{POSTGRES_USER_NAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
engine = sa.create_engine(db, echo=False)


# -----------------------------------------------------------------------------
# DATABASE CONNECTION: layers
# -----------------------------------------------------------------------------
POSTGRES_DB_LAYERS = "layers"
TABLE_NAME_WELL = "well"
TABLE_NAME_AQUIFER = "aquifer"
TABLE_NAME_MAHDOUDE = "mahdoude"

db_layers = f"postgresql://{POSTGRES_USER_NAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_LAYERS}"
engine_layers = sa.create_engine(db_layers, echo=False)


# -----------------------------------------------------------------------------
# FUNCTION: FIND TABLE
# -----------------------------------------------------------------------------
def find_table(
    database,
    table,
    user,
    password,
    host,
    port,
):
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True    
    cursor = conn.cursor()    
    sql = '''SELECT table_name FROM information_schema.tables;'''
    cursor.execute(sql)
    table_name_list_exist = list(itertools.chain.from_iterable(cursor.fetchall()))
    conn.close()
    
    if table in table_name_list_exist:
        return True
    else:
        return False