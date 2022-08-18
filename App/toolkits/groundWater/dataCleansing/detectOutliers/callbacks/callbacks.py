import os
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashLogger
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_datatables as ddt
from . import *



def toolkits__groundWater__dataCleansing__detectOutliers__callbacks(app):
    
    @app.callback(
        Output('MAP', 'figure'),
        Input('INTERVAL', 'n_intervals'),
    )
    def map(
        n
    ):
        if n:
            return BASE_MAP
        else:
            return BASE_MAP



    @app.callback(
        Output('STUDY_AREA_SELECT', 'options'),
        Input('INTERVAL', 'n_intervals'),
    )
    def study_area_select(
        n
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
        
        if "geoinfo" in table_name_list_exist:
    
            df = pd.read_sql_query(
                sql='SELECT DISTINCT "MAHDOUDE_NAME" FROM geoinfo;',
                con=engine
            )
        
            return [{'label': i, 'value': i} for i in df.MAHDOUDE_NAME.values]
        else:
            return [{}]



    @app.callback(
        Output('AQUIFER_SELECT', 'options'),
        Input('STUDY_AREA_SELECT', 'value'),
    )
    def aquifer_select(
        study_area_selected
    ):
        if study_area_selected is not None and len(study_area_selected) != 0:
            df = pd.read_sql_query(
                sql=f'SELECT DISTINCT "MAHDOUDE_NAME", "AQUIFER_NAME" FROM geoinfo;',
                con=engine
            )
            df = df[df["MAHDOUDE_NAME"].isin(study_area_selected)]
            return [{'label': i, 'value': i} for i in df.AQUIFER_NAME.values]
        else:
            return [{}]



    @app.callback(
        Output('WELL_SELECT', 'options'),
        Input('AQUIFER_SELECT', 'value'),
        Input('STUDY_AREA_SELECT', 'value'),
    )
    def well_select(
        aquifer_selected,
        study_area_selected
    ):
        if study_area_selected is not None and len(study_area_selected) != 0:
            if aquifer_selected is not None and len(aquifer_selected) != 0:
                df = pd.read_sql_query(
                    sql=f'SELECT DISTINCT "MAHDOUDE_NAME", "AQUIFER_NAME", "LOCATION_NAME" FROM geoinfo;',
                    con=engine
                )
                df = df[df["MAHDOUDE_NAME"].isin(study_area_selected)]
                df = df[df["AQUIFER_NAME"].isin(aquifer_selected)]
                return [{'label': i, 'value': i} for i in df.LOCATION_NAME.values]
            else:
                return [{}]
        else:
            return [{}]
