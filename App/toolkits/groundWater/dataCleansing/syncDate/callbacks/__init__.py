import itertools
import numpy as np
import pandas as pd
import sqlalchemy as sa
import psycopg2
import plotly.graph_objects as go
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from App.db import *


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
# FUNCTION SYNC DATE
# -----------------------------------------------------------------------------
def f_syncdate(
    df,
    day
):
    if day != 0:
        
        df = df.sort_values(by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]).reset_index(drop=True)
        
        tmp = df[["DATE_GREGORIAN", "WATER_TABLE"]].set_index('DATE_GREGORIAN').resample('D').mean().interpolate('linear').reset_index(drop=False)
        
        day_persian_start = df["DAY_PERSIAN"].iloc[0]
        day_persian_end = df["DAY_PERSIAN"].iloc[-1]
        n = len(df)
        cols_p = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
        cols_g = ['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']
        
        df["DAY_PERSIAN"] = day
        df.loc[0, 'DAY_PERSIAN'] = day_persian_start
        df.loc[n-1, 'DAY_PERSIAN'] = day_persian_end
        
        df[cols_p] = df[cols_p].apply(pd.to_numeric, errors='coerce')
        df[cols_p] = df[cols_p].astype(pd.Int64Dtype())        
        date_persian, date_gregorian = np.vectorize(ymd_persian_to_date)(df.YEAR_PERSIAN, df.MONTH_PERSIAN, df.DAY_PERSIAN)
        
        df["DATE_PERSIAN"] = list(date_persian)
        df["DATE_GREGORIAN"] = list(date_gregorian)
        
        df[cols_p] = df['DATE_PERSIAN'].str.split('-', 2, expand=True)
        df[cols_g] = df['DATE_GREGORIAN'].astype(str).str.split('-', 2, expand=True)
        
        df["YEAR_PERSIAN"] = df["YEAR_PERSIAN"].astype(str).str.zfill(4)
        df["MONTH_PERSIAN"] = df["MONTH_PERSIAN"].astype(str).str.zfill(2)
        df["DAY_PERSIAN"] = df["DAY_PERSIAN"].astype(str).str.zfill(2)
        df["YEAR_GREGORIAN"] = df["YEAR_GREGORIAN"].str.zfill(4)
        df["MONTH_GREGORIAN"] = df["MONTH_GREGORIAN"].str.zfill(2)
        df["DAY_GREGORIAN"] = df["DAY_GREGORIAN"].str.zfill(2)
        df['DATE_PERSIAN'] = df["YEAR_PERSIAN"] + "-" + df["MONTH_PERSIAN"] + "-" + df["DAY_PERSIAN"]
        df['DATE_GREGORIAN'] = df["YEAR_GREGORIAN"] + "-" + df["MONTH_GREGORIAN"] + "-" + df["DAY_GREGORIAN"]
        df["DATE_GREGORIAN"] = df["DATE_GREGORIAN"].apply(pd.to_datetime)
        
        df_columns = df.columns
        
        df = df.drop(['WATER_TABLE'], axis=1)
        
        result = df.merge(tmp, on=["DATE_GREGORIAN"], how="left")
        
        result = result[df_columns]
        
        return result
    
    else:
        
        return df


# -----------------------------------------------------------------------------
# FUNCTION CONVERT DAY, MONTH, YEAR PERSIAN TO DATE
# -----------------------------------------------------------------------------
def ymd_persian_to_date(
    year,
    month,
    day,
):
    try:
        date_persian = str(year) + "-" + str(month) + "-" + str(day)
        date_gregorian = JalaliDate(year, month, day).to_gregorian()
        return date_persian, date_gregorian
    except:
        return pd.NA, pd.NA
    
    
# -----------------------------------------------------------------------------
# FUNCTION FIND TABLE
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


# -----------------------------------------------------------------------------
# FUNCTION UPDATE TABLE
# -----------------------------------------------------------------------------
def update_table(
    data,
    table_exist,
    table_name,
    engine,
    study_area=None,
    aquifer=None,
    well=None,
):

    if table_exist:
        
        data_exist = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name}",
            con=engine
        )
        
        if (study_area is not None) and (aquifer is not None) and (well is not None):
            df = data_exist.drop(
                data_exist[(data_exist['MAHDOUDE'] == study_area) & (data_exist['AQUIFER'] == aquifer) & (data_exist['LOCATION'] == well)].index
            ).reset_index(drop=True)
        elif (study_area is not None) and (aquifer is not None) and (well is None):
            df = data_exist.drop(
                data_exist[(data_exist['MAHDOUDE'] == study_area) & (data_exist['AQUIFER'] == aquifer)].index
            ).reset_index(drop=True)
        elif (study_area is not None) and (aquifer is None) and (well is None):
            df = data_exist.drop(
                data_exist[(data_exist['MAHDOUDE'] == study_area)].index
            ).reset_index(drop=True)
        else:
            df = pd.DataFrame(columns=data_exist.columns)
        
        data = pd.concat(
            [df, data]
        ).drop_duplicates().sort_values(
            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
        ).reset_index(drop=True)
        
        data.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )
        
    else:
        
        data.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',
            index=False
        )


# -----------------------------------------------------------------------------
# FUNCTION UPDATE TABLE DATA
# -----------------------------------------------------------------------------
def update_table_data(
    table_name_syncdate,
    table_name_data,
    engine,
    database,
    user,
    password,
    host,
    port
):
    table_syncdate_exist = find_table(
        database=database,
        table=table_name_syncdate,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    if table_syncdate_exist:

        data_syncdate = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name_syncdate}",
            con=engine
        )
        
        data = data_syncdate.dropna(subset=['WATER_TABLE']).drop_duplicates()
        
        data_geoinfo = pd.read_sql_query(
            sql=f"SELECT * FROM {DB_DATA_TABLE_GEOINFO}",
            con=engine
        )
        
        data = data.merge(
            right=data_geoinfo[["MAHDOUDE", "AQUIFER", "LOCATION", "LEVEL_SRTM"]],
            how="left",
            on=["MAHDOUDE", "AQUIFER", "LOCATION"],
        )
        
        data["WATER_LEVEL"] = data["LEVEL_SRTM"] - data["WATER_TABLE"]
            
        data.drop(
            columns=["LEVEL_SRTM"],
            inplace=True
        )
        
        data = data.sort_values(
            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
        ).reset_index(drop=True)
        
        data.to_sql(
            name=table_name_data,
            con=engine,
            if_exists='replace',
            index=False
        )