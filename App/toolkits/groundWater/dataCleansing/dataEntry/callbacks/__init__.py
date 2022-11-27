import base64
import os
import io
import shutil
import tempfile
import pandas as pd
import geopandas as gpd
import zipfile
import psycopg2
import itertools
from sqlalchemy import *
import Assets.jalali as jalali
import plotly.graph_objects as go
from geoalchemy2 import Geometry, WKTElement
from shapely import wkt, wkb
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from App.db import *


# -----------------------------------------------------------------------------
# CONSTANT VARIABLES
# -----------------------------------------------------------------------------
PATH_THEMPLATE_FILE = "./Assets/Files/HydrographDataTemplate.xlsx"
PATH_UPLOADED_FILES = "./Assets/Files/Uploaded_Files"
SORT_COLUMNS = ["MAHDOUDE", "AQUIFER", "LOCATION"]


def read_shapefile_from_zip_file(
    contents,
    filename,
    path_uploaded_files,
    srid,
):
    if filename.endswith(".zip"):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        zip_file_str = io.BytesIO(decoded)
        zip_file = zipfile.ZipFile(zip_file_str, 'r')
        zip_file.extractall(path_uploaded_files)
        zip_file.close()
        
        for i in os.listdir(path_uploaded_files):
            if os.path.isdir(f"{path_uploaded_files}/{i}"):
                for j in os.listdir(f"{path_uploaded_files}/{i}"):
                    if j.endswith(".shp"):
                        tmp = gpd.read_file(f"{path_uploaded_files}/{i}/{j}")
                shutil.rmtree(f"{path_uploaded_files}/{i}")
            elif i.endswith(".shp"):
                tmp = gpd.read_file(f"{path_uploaded_files}/{i}")
        
        for i in os.listdir(path_uploaded_files):
            os.remove(f"{path_uploaded_files}/{i}")
        
        func = lambda geom: wkb.loads(wkb.dumps(geom, output_dimension=2))
        tmp['geometry'] = tmp['geometry'].apply(func)

        tmp = tmp.to_crs({'init': f'epsg:{srid}'})
        tmp['geometry'] = tmp['geometry'].apply(lambda x: WKTElement(x.wkt, srid = srid))

        return tmp
    
    else:
        
        return None

def check_replace_append(
    data,
    db,
    table,
    engine,
    if_exists,
    geometry_type,
    srid,
    geom_col,
    sort_columns,
):
    
    conn = psycopg2.connect(
        database=db,
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
    
    if (if_exists == 'replace') or (table not in table_name_list_exist):
        
        data = data.drop_duplicates().sort_values(
            by=sort_columns
        ).reset_index(drop=True)
        
        data[geom_col] = data[geom_col].astype(str).apply(wkt.loads)
        
        data = gpd.GeoDataFrame(
            data=data,
            geometry=geom_col,
            crs=f"EPSG:{srid}"
        )
        
        data.to_postgis(
            table,
            engine,
            if_exists="replace",
            index=False,
            dtype={'geometry': Geometry(geometry_type=geometry_type, srid=srid)}
        )

    else:
        
        sql = f"SELECT * FROM {table}"
        
        data_exist = gpd.GeoDataFrame.from_postgis(
            sql=sql,
            con=engine,
            geom_col=geom_col
        )
        
        data = pd.concat(
                [data_exist, data],
                ignore_index=True
        )
        
        data[geom_col] = data[geom_col].astype(str).apply(wkt.loads)
        
        data = gpd.GeoDataFrame(
            data=data,
            geometry=geom_col,
            crs=f"EPSG:{srid}"
        )
        
        data = data.drop_duplicates().sort_values(
            by=sort_columns
        ).reset_index(drop=True)
        
        data.to_postgis(
            table,
            engine,
            if_exists="replace",
            index=False,
            dtype={'geometry': Geometry(geometry_type=geometry_type, srid=srid)}
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
    geoinfo_data[COLs] = geoinfo_data[COLs].apply(lambda x: x.str.rstrip())
    geoinfo_data[COLs] = geoinfo_data[COLs].apply(lambda x: x.str.lstrip())
    geoinfo_data[COLs] = geoinfo_data[COLs].apply(lambda x: x.str.replace('ي','ی'))
    geoinfo_data[COLs] = geoinfo_data[COLs].apply(lambda x: x.str.replace('ئ','ی'))
    geoinfo_data[COLs] = geoinfo_data[COLs].apply(lambda x: x.str.replace('ك', 'ک'))
    
    geoinfo_data = geoinfo_data.drop_duplicates(subset=geoinfo_data_column.difference(['ID'])).sort_values(
        by=["MAHDOUDE", "AQUIFER", "LOCATION"]
    ).reset_index(drop=True)
    
    conn = psycopg2.connect(
                database=POSTGRES_DB_DATA,
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
    persian_modified_columns=['MAHDOUDE', 'AQUIFER', 'LOCATION'],
    sort_columns=SORT_COLUMNS,
):
    raw_data = raw_data[raw_data_column]
    COLs = persian_modified_columns
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.rstrip())
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.lstrip())
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.replace('ي','ی'))
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.replace('ئ','ی'))
    raw_data[COLs] = raw_data[COLs].apply(lambda x: x.str.replace('ك', 'ک'))

    raw_data = raw_data.drop_duplicates().sort_values(
        by=sort_columns
    ).reset_index(drop=True)
    
    raw_data['DESCRIPTION'] = raw_data['DESCRIPTION'].fillna("")

    conn = psycopg2.connect(
                database=POSTGRES_DB_DATA,
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
            by=sort_columns
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
    sort_columns=SORT_COLUMNS,
):
    conn = psycopg2.connect(
                database=POSTGRES_DB_DATA,
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
            by=sort_columns
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
            by=sort_columns
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
    

def create_update_modified_data_table(
    engine,
    if_exists,
    table_name_raw_data=DB_DATA_TABLE_RAWDATA,
    table_name_modified_data=DB_DATA_TABLE_MODIFIEDDATA,
    table_name_raw_data_deleted=DB_DATA_TABLE_RAW_DATA_DELETED,
    table_name_raw_data_modified=DB_DATA_TABLE_RAW_DATA_MODIFIED,
    sort_columns=SORT_COLUMNS,
):
    conn = psycopg2.connect(
                database=POSTGRES_DB_DATA,
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
    
    if (table_name_modified_data not in table_name_list_exist) or (if_exists == "replace"):
        
        raw_data = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name_raw_data}",
            con=engine
        )
        
        raw_data.to_sql(
            name=table_name_modified_data,
            con=engine,
            if_exists='replace',
            index=False
        )
        
        # tmp = pd.DataFrame(
        #     columns=raw_data.columns
        # )
        
        # tmp.to_sql(
        #     name=table_name_raw_data_deleted,
        #     con=engine,
        #     if_exists='replace',
        #     index=False
        # )
        
        # tmp.to_sql(
        #     name=table_name_raw_data_modified,
        #     con=engine,
        #     if_exists='replace',
        #     index=False
        # )
    
    else:
        
        raw_data = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name_raw_data}",
            con=engine
        )
        
        modified_data = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name_modified_data}",
            con=engine
        )
        
        raw_data_deleted = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name_raw_data_deleted}",
            con=engine
        )
        
        raw_data_modified = pd.read_sql_query(
            sql=f"SELECT * FROM {table_name_raw_data_modified}",
            con=engine
        )
        
        tmp = pd.concat([raw_data, raw_data_deleted, raw_data_modified]).drop_duplicates(keep=False).sort_values(
            by=sort_columns
        ).reset_index(drop=True)
        
        tmp = pd.concat([modified_data, tmp]).drop_duplicates(keep="last").sort_values(
            by=sort_columns
        ).reset_index(drop=True)
        
        tmp.to_sql(
            name=table_name_modified_data,
            con=engine,
            if_exists='replace',
            index=False
        )


def delete_table():    
   
    conn = psycopg2.connect(
        database=POSTGRES_DB_DATA,
        user=POSTGRES_USER_NAME,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    
    conn.autocommit = True
    
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_GEOINFO}")
    except:
        pass
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_RAWDATA}")
    except:
        pass
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_RAW_DATA_DELETED}")
    except:
        pass
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_RAW_DATA_MODIFIED}")
    except:
        pass
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_MODIFIEDDATA}")
    except:
        pass
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_INTERPOLATEDDATA}")
    except:
        pass
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_SYNCDATEDATA}")
    except:
        pass
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_DATA}")
    except:
        pass
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_HYDROGRAPH}")
    except:
        pass
    try:
        cursor.execute(f"DROP TABLE {DB_DATA_TABLE_TEMPORARY}")
    except:
        pass
    
    conn.commit()
    
    conn.close()