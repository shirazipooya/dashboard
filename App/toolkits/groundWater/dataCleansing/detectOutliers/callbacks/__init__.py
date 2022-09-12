import base64
import io
import pandas as pd
import psycopg2
import itertools
import plotly.graph_objects as go
from sqlalchemy import *
import Assets.jalali as jalali
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from App.db import POSTGRES_USER_NAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT



# -----------------------------------------------------------------------------
# CONSTANT VARIABLES
# -----------------------------------------------------------------------------
PATH_THEMPLATE_FILE = "./Assets/Files/HydrographDataTemplate.xlsx"

PATH_UPLOADED_FILES = "./Assets/Files/Uploaded_Files"

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
# DATABASE CONNECTION: data
# -----------------------------------------------------------------------------
POSTGRES_DB_NAME = "data"
TABLE_NAME_RAW_DATA = "raw_data"
TABLE_NAME_MODIFIED_DATA = "modified_data"
TABLE_NAME_RAW_DATA_DELETED = "raw_data_deleted"
TABLE_NAME_RAW_DATA_MODIFIED = "raw_data_modified"

db = f"postgresql://{POSTGRES_USER_NAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
engine = create_engine(db, echo=False)


# -----------------------------------------------------------------------------
# DATABASE CONNECTION: layers
# -----------------------------------------------------------------------------
POSTGRES_DB_LAYERS = "layers"
db_layers = f"postgresql://{POSTGRES_USER_NAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_LAYERS}"
engine_layers = create_engine(db_layers, echo=False)


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



def read_data_from_spreadsheet(
    contents,
    filename
):
    if '.xlsx' in filename or '.xls' in filename:
        data = {}
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        spreadsheet_file = pd.ExcelFile(io.BytesIO(decoded))
        if len(spreadsheet_file.sheet_names) >= 2:
            for sheet_name in spreadsheet_file.sheet_names:
                data[sheet_name] = spreadsheet_file.parse(sheet_name).to_dict()
            return data, spreadsheet_file.sheet_names
        else:
            return None, None


def create_geoinfo_data_table(
    geoinfo_data,
    engine,
    table_name,
    geoinfo_data_column,
    if_exists
):
    geoinfo_data = geoinfo_data[geoinfo_data_column]
    COLs = ['MAHDOUDE', 'AQUIFER', 'LOCATION']
    geoinfo_data[COLs].apply(lambda x: x.str.rstrip())
    geoinfo_data[COLs] = geoinfo_data[COLs].apply(lambda x: x.str.lstrip())
    geoinfo_data[COLs] = geoinfo_data[COLs].apply(lambda x: x.str.replace('ي','ی'))
    geoinfo_data[COLs] = geoinfo_data[COLs].apply(lambda x: x.str.replace('ئ','ی'))
    geoinfo_data[COLs] = geoinfo_data[COLs].apply(lambda x: x.str.replace('ك', 'ک'))
    
    geoinfo_data = geoinfo_data.drop_duplicates(subset=geoinfo_data_column.difference(['ID'])).sort_values(
        by=["MAHDOUDE", "AQUIFER", "LOCATION"]
    ).reset_index(drop=True)
    
    conn = psycopg2.connect(
                database=POSTGRES_DB_NAME,
                user=POSTGRES_USER_NAME,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT
            )    
    conn.autocommit = True    
    cursor = conn.cursor()    
    sql = '''SELECT table_name FROM information_schema.tables;'''
    cursor.execute(sql)
    table_name_list_exist = list(itertools.chain.from_iterable(cursor.fetchall()))
    conn.close()
    
    if (if_exists == 'replace') or (table_name not in table_name_list_exist):
        geoinfo_data.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )
    else:
        geoinfo_data_exist = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name}",
            con=engine
        )
                    
        geoinfo_data = pd.concat(
            [geoinfo_data_exist, geoinfo_data]
        ).drop_duplicates(subset=geoinfo_data_exist.columns.difference(['ID'])).sort_values(
            by=["MAHDOUDE", "AQUIFER", "LOCATION"]
        ).reset_index(drop=True)
        
        geoinfo_data.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )


def create_raw_data_table(
    raw_data,
    engine,
    table_name,
    raw_data_column,
    if_exists,
    date_type,
):
    raw_data = raw_data[raw_data_column]
    COLs = ['MAHDOUDE', 'AQUIFER', 'LOCATION']
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.rstrip())
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.lstrip())
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.replace('ي','ی'))
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.replace('ئ','ی'))
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.replace('ك', 'ک'))

    if date_type == "persian_ymd":
        raw_data["YEAR_PERSIAN"] = raw_data["YEAR_PERSIAN"].astype(str).str.zfill(4)
        raw_data["MONTH_PERSIAN"] = raw_data["MONTH_PERSIAN"].astype(str).str.zfill(2)
        raw_data["DAY_PERSIAN"] = raw_data["DAY_PERSIAN"].astype(str).str.zfill(2)
        raw_data['DATE_PERSIAN'] = raw_data["YEAR_PERSIAN"] + "-" + raw_data["MONTH_PERSIAN"] + "-" + raw_data["DAY_PERSIAN"]
        raw_data['DATE_GREGORIAN'] = raw_data.apply(
            lambda x: jalali.Persian(x["DATE_PERSIAN"]).gregorian_string(), 
            axis=1
        )
        raw_data[['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']] = raw_data['DATE_GREGORIAN'].str.split('-', 2, expand=True)
        raw_data["YEAR_GREGORIAN"] = raw_data["YEAR_GREGORIAN"].str.zfill(4)
        raw_data["MONTH_GREGORIAN"] = raw_data["MONTH_GREGORIAN"].str.zfill(2)
        raw_data["DAY_GREGORIAN"] = raw_data["DAY_GREGORIAN"].str.zfill(2)
        raw_data["DATE_GREGORIAN"] = raw_data["DATE_GREGORIAN"].apply(pd.to_datetime)
        
    elif date_type == "gregorian_ymd":
        raw_data["YEAR_GREGORIAN"] = raw_data["YEAR_GREGORIAN"].astype(str).str.zfill(4)
        raw_data["MONTH_GREGORIAN"] = raw_data["MONTH_GREGORIAN"].astype(str).str.zfill(2)
        raw_data["DAY_GREGORIAN"] = raw_data["DAY_GREGORIAN"].astype(str).str.zfill(2)
        raw_data['DATE_GREGORIAN'] = raw_data["YEAR_GREGORIAN"] + "-" + raw_data["MONTH_GREGORIAN"] + "-" + raw_data["DAY_GREGORIAN"]
        raw_data["DATE_GREGORIAN"] = raw_data["DATE_GREGORIAN"].apply(pd.to_datetime)
        raw_data['DATE_PERSIAN'] = raw_data.apply(
            lambda x: jalali.Gregorian(x["DATE_GREGORIAN"].date()).persian_string(), 
            axis=1
        )
        raw_data[['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']] = raw_data['DATE_PERSIAN'].str.split('-', 2, expand=True)
        raw_data["YEAR_PERSIAN"] = raw_data["YEAR_PERSIAN"].str.zfill(4)
        raw_data["MONTH_PERSIAN"] = raw_data["MONTH_PERSIAN"].str.zfill(2)
        raw_data["DAY_PERSIAN"] = raw_data["DAY_PERSIAN"].str.zfill(2)
    
    elif date_type == "persian_date":
        raw_data[['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']] = raw_data['DATE_PERSIAN'].str.split('-', 2, expand=True)
        raw_data["YEAR_PERSIAN"] = raw_data["YEAR_PERSIAN"].str.zfill(4)
        raw_data["MONTH_PERSIAN"] = raw_data["MONTH_PERSIAN"].str.zfill(2)
        raw_data["DAY_PERSIAN"] = raw_data["DAY_PERSIAN"].str.zfill(2)
        raw_data['DATE_PERSIAN'] = raw_data["YEAR_PERSIAN"] + "-" + raw_data["MONTH_PERSIAN"] + "-" + raw_data["DAY_PERSIAN"]
        raw_data['DATE_GREGORIAN'] = raw_data.apply(
            lambda x: jalali.Persian(x["DATE_PERSIAN"]).gregorian_string(), 
            axis=1
        )
        raw_data[['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']] = raw_data['DATE_GREGORIAN'].str.split('-', 2, expand=True)
        raw_data["YEAR_GREGORIAN"] = raw_data["YEAR_GREGORIAN"].str.zfill(4)
        raw_data["MONTH_GREGORIAN"] = raw_data["MONTH_GREGORIAN"].str.zfill(2)
        raw_data["DAY_GREGORIAN"] = raw_data["DAY_GREGORIAN"].str.zfill(2)
        raw_data["DATE_GREGORIAN"] = raw_data["DATE_GREGORIAN"].apply(pd.to_datetime)
    
    elif date_type == "gregorian_date":
        raw_data[['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']] = raw_data['DATE_GREGORIAN'].str.split('-', 2, expand=True)
        raw_data["YEAR_GREGORIAN"] = raw_data["YEAR_GREGORIAN"].str.zfill(4)
        raw_data["MONTH_GREGORIAN"] = raw_data["MONTH_GREGORIAN"].str.zfill(2)
        raw_data["DAY_GREGORIAN"] = raw_data["DAY_GREGORIAN"].str.zfill(2)
        raw_data['DATE_GREGORIAN'] = raw_data["YEAR_GREGORIAN"] + "-" + raw_data["MONTH_GREGORIAN"] + "-" + raw_data["DAY_GREGORIAN"]
        raw_data["DATE_GREGORIAN"] = raw_data["DATE_GREGORIAN"].apply(pd.to_datetime)
        raw_data['DATE_PERSIAN'] = raw_data.apply(
            lambda x: jalali.Gregorian(x["DATE_GREGORIAN"].date()).persian_string(), 
            axis=1
        )
        raw_data[['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']] = raw_data['DATE_PERSIAN'].str.split('-', 2, expand=True)
        raw_data["YEAR_PERSIAN"] = raw_data["YEAR_PERSIAN"].str.zfill(4)
        raw_data["MONTH_PERSIAN"] = raw_data["MONTH_PERSIAN"].str.zfill(2)
        raw_data["DAY_PERSIAN"] = raw_data["DAY_PERSIAN"].str.zfill(2)
    else:
        pass
    
    raw_data = raw_data.drop_duplicates().sort_values(
        by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
    ).reset_index(drop=True)  

    conn = psycopg2.connect(
                database=POSTGRES_DB_NAME,
                user=POSTGRES_USER_NAME,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT
            )    
    conn.autocommit = True    
    cursor = conn.cursor()    
    sql = '''SELECT table_name FROM information_schema.tables;'''
    cursor.execute(sql)
    table_name_list_exist = list(itertools.chain.from_iterable(cursor.fetchall()))
    conn.close()
    
    if (if_exists == 'replace') or (table_name not in table_name_list_exist):
        raw_data.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )
    else:
        raw_data_exist = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name}",
            con=engine
        )
        
        raw_data = pd.concat(
            [raw_data_exist, raw_data]
        ).drop_duplicates().sort_values(
            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
        ).reset_index(drop=True)
        
        raw_data.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )


def clean_geoinfo_raw_data_table(
    engine,
    table_name_geoinfo,
    table_name_raw_data,
):
    conn = psycopg2.connect(
                database=POSTGRES_DB_NAME,
                user=POSTGRES_USER_NAME,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT
            )    
    conn.autocommit = True    
    cursor = conn.cursor()    
    sql = '''SELECT table_name FROM information_schema.tables;'''
    cursor.execute(sql)
    table_name_list_exist = list(itertools.chain.from_iterable(cursor.fetchall()))
    conn.close()
    
    if (table_name_geoinfo in table_name_list_exist) and (table_name_raw_data in table_name_list_exist):
        
        geoinfo_data = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name_geoinfo}",
            con=engine
        )
        
        raw_data = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name_raw_data}",
            con=engine
        )
        
        geoinfo_data_tmp = geoinfo_data.copy()
        geoinfo_data_tmp = geoinfo_data_tmp[["MAHDOUDE", "AQUIFER", "LOCATION"]]
        geoinfo_data_tmp['MARKER'] = 1
        
        raw_data = pd.merge(raw_data, geoinfo_data_tmp, on=["MAHDOUDE", "AQUIFER", "LOCATION"], how='left')
        raw_data = raw_data[~pd.isnull(raw_data['MARKER'])]
        raw_data = raw_data.reset_index(drop=True)
        raw_data = raw_data.drop(columns=['MARKER'])
        raw_data = raw_data.sort_values(
            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
        ).reset_index(drop=True)
        
        raw_data_tmp = raw_data.copy()
        raw_data_tmp = raw_data_tmp.drop_duplicates(subset=["MAHDOUDE", "AQUIFER", "LOCATION"]).reset_index(drop=True)
        raw_data_tmp = raw_data_tmp[["MAHDOUDE", "AQUIFER", "LOCATION"]]
        raw_data_tmp['MARKER'] = 1
        
        geoinfo_data = pd.merge(geoinfo_data, raw_data_tmp, on=["MAHDOUDE", "AQUIFER", "LOCATION"], how='left')
        geoinfo_data = geoinfo_data[~pd.isnull(geoinfo_data['MARKER'])]
        geoinfo_data = geoinfo_data.reset_index(drop=True)
        geoinfo_data = geoinfo_data.drop(columns=['MARKER'])
        geoinfo_data = geoinfo_data.sort_values(
            by=["MAHDOUDE", "AQUIFER", "LOCATION"]
        ).reset_index(drop=True)
        
        geoinfo_data.to_sql(
            name=table_name_geoinfo,
            con=engine,
            if_exists='replace',
            index=False
        )
        
        raw_data.to_sql(
            name=table_name_raw_data,
            con=engine,
            if_exists='replace',
            index=False
        )
        
    else:
        pass


def check_persian_date_ymd(
    year_persian,
    month_persian,
    day_persian,
):
    try:
        date_persian = str(year_persian) + "-" + str(month_persian) + "-" + str(day_persian)
        date_gregorian = JalaliDate(year_persian, month_persian, day_persian).to_gregorian()
        return date_persian, date_gregorian
    except:
        return pd.NA, pd.NA
