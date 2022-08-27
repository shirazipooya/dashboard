from distutils.command.config import dump_file
import os
import json
from unittest import result
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import pandas as pd
import numpy as np
import geopandas as gpd
import dash_bootstrap_components as dbc
from dash import dash_table, html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashLogger
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_datatables as ddt
import plotly.graph_objects as go
import plotly.express as px
from . import *



def toolkits__groundWater__dataCleansing__detectOutliers__callbacks(app):
    
    @app.callback(
        Output('MAP', 'figure'),
        Input('INTERVAL', 'n_intervals'),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
    )
    def map(
        n, study_area, aquifer, well
    ):
        if well is not None and len(well) != 0:
            
            # MAHDOUDE
            if len(study_area) == 1:
                sql = f"SELECT * FROM mahdoude WHERE \"MAHDOUDE\" = '{study_area[0]}'"
            else:
                sql = f'SELECT * FROM mahdoude WHERE "MAHDOUDE" IN {*study_area,}'
            
            df_study_area = gpd.GeoDataFrame.from_postgis(
                sql=sql,
                con=engine_layers,
                geom_col="geometry"
            )
            
            df_study_area_json = json.loads(df_study_area.to_json())
            
            for feature in df_study_area_json["features"]:
                feature['id'] = feature['properties']['MAHDOUDE']
            
            # AQUIFER            
            if len(aquifer) == 1:
                sql = f"SELECT * FROM aquifer WHERE \"AQUIFER\" = '{aquifer[0]}'"
            else:
                sql = f'SELECT * FROM aquifer WHERE "AQUIFER" IN {*aquifer,}'
            
            df_aquifer = gpd.GeoDataFrame.from_postgis(
                sql=sql,
                con=engine_layers,
                geom_col="geometry"
            )
            
            df_aquifer_json = json.loads(df_aquifer.to_json())
            
            for feature in df_aquifer_json["features"]:
                feature['id'] = feature['properties']['AQUIFER']
            
            # WELL
            if len(well) == 1:
                sql = f"SELECT * FROM well WHERE \"LOCATION\" = '{well[0]}'"
            else:
                sql = f'SELECT * FROM well WHERE "LOCATION" IN {*well,}'
            
            df_well = gpd.GeoDataFrame.from_postgis(
                sql=sql,
                con=engine_layers,
                geom_col="geometry"
            )
            
            # ALL WELL
            if len(study_area) == 1 and len(aquifer) == 1:
                sql = f"SELECT * FROM well WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}'"
            elif len(study_area) != 1 and len(aquifer) == 1:
                sql = f"SELECT * FROM well WHERE (\"MAHDOUDE\" IN {*study_area,}' AND \"AQUIFER\" = '{aquifer[0]}'"
            elif len(study_area) == 1 and len(aquifer) != 1:
                sql = f"SELECT * FROM well WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,}"
            else:
                sql = f'SELECT * FROM well WHERE ("MAHDOUDE" IN {*study_area,} AND "AQUIFER" IN {*aquifer,})'
            
            df_all_well = gpd.GeoDataFrame.from_postgis(
                sql=sql,
                con=engine_layers,
                geom_col="geometry"
            )
            
            fig = px.choropleth_mapbox(
                data_frame=df_study_area,
                geojson=df_study_area_json,
                locations="MAHDOUDE",
                hover_name="MAHDOUDE",
                hover_data={"MAHDOUDE": False},
                opacity=0.4,
            )
            
            fig2 = px.choropleth_mapbox(
                data_frame=df_aquifer,
                geojson=df_aquifer_json,
                locations="AQUIFER",
                hover_name="AQUIFER",
                hover_data={"MAHDOUDE": True, "AQUIFER": False},
                opacity=0.7,
                labels={'MAHDOUDE':'محدوده مطالعاتی', 'AQUIFER':'آبخوان'},                
            )
            
            fig.add_trace(fig2.data[0])
            
            for i, frame in enumerate(fig.frames):
                fig.frames[i].data += (fig2.frames[i].data[0],)

            
            fig.add_trace(
                go.Scattermapbox(
                    lat=df_all_well.Y,
                    lon=df_all_well.X,
                    mode='markers',
                    marker=go.scattermapbox.Marker(size=8, color="red"),
                    text=df_all_well["LOCATION"],
                    hoverinfo='text',
                    hovertemplate='<span style="color:white;">%{text}</span><extra></extra>'
                )
            )
            
            fig.add_trace(
                go.Scattermapbox(
                    lat=df_well.Y,
                    lon=df_well.X,
                    mode='markers',
                    marker=go.scattermapbox.Marker(size=12, color="green"),
                    text=df_well["LOCATION"],
                    hoverinfo='text',
                    hovertemplate='<span style="color:white;">%{text}</span><extra></extra>'
                )
            )
            
            fig.update_layout(
                mapbox = {
                    'style': "stamen-terrain",
                    'zoom': 7,
                    'center': {
                        'lat': df_well.Y.mean(),
                        'lon': df_well.X.mean(),
                    },
                },
                showlegend = False,
                hovermode='closest',
                margin = {'l':0, 'r':0, 'b':0, 't':0}
            )
            
            return fig
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
                sql='SELECT DISTINCT "MAHDOUDE" FROM geoinfo;',
                con=engine
            )
        
            return [{'label': i, 'value': i} for i in sorted(df.MAHDOUDE.values)]
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
                sql=f'SELECT DISTINCT "MAHDOUDE", "AQUIFER" FROM geoinfo;',
                con=engine
            )
            df = df[df["MAHDOUDE"].isin(study_area_selected)]
            return [{'label': i, 'value': i} for i in sorted(df.AQUIFER.values)]
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
                    sql=f'SELECT DISTINCT "MAHDOUDE", "AQUIFER", "LOCATION" FROM geoinfo;',
                    con=engine
                )
                df = df[df["MAHDOUDE"].isin(study_area_selected)]
                df = df[df["AQUIFER"].isin(aquifer_selected)]
                return [{'label': i, 'value': i} for i in sorted(df.LOCATION.values)]
            else:
                return [{}]
        else:
            return [{}]
    
    
    
    @app.callback(
        Output('BUTTON_STAGE_1', 'n_clicks'),
        Output('STORAGE', 'data'),
        Output("ALERTS", "children"),
        Input('BUTTON_STAGE_1', 'n_clicks'),
        Input('SELECT_DATE_TYPE', 'value'),        
        State('STORAGE', 'data'),
        State('TABLE_ERROR_DATE', 'data'),
    )
    def show_wrong_date(
        n_clicks, date_type_value, storage_state, data_table_state
    ):
        if n_clicks != 0:
            
            print(storage_state)
            
            if storage_state["raw_data"]:
                
                df = pd.read_sql_query(
                    sql = f"SELECT * FROM raw_data",
                    con = engine
                ).reset_index().rename(columns = {'index':'idx'})
                
                df = df.drop(storage_state["index_wrong_date"])

                df = pd.concat([df, pd.DataFrame(data_table_state)]).reset_index(drop=True).drop(columns=['idx'])
                
                df.to_sql(
                    name="raw_data",
                    con=engine,
                    if_exists='replace',
                    index=False
                )
                
            
                
        
        else:
            
            notify = dmc.Notification(
                id ="notify",
                title = "",
                message = [""],
                color = 'red',
                action = "hide",
            )
                    
            result = [
                0,
                storage_state,
                notify,
            ]
            
            return result
            
    
    
    
    
    @app.callback(
        Output('BUTTON_SHOW_WRONG_DATE', 'n_clicks'),
        Output('DIV_TABLE_ERROR_DATE', 'hidden'),
        Output('TABLE_ERROR_DATE', 'data'),
        Output('TABLE_ERROR_DATE', 'columns'),
        Output("ALERTS", "children"),
        Output("STORAGE", "data"),
        Input('BUTTON_SHOW_WRONG_DATE', 'n_clicks'),
        Input('INTERVAL', 'n_intervals'),
        Input('SELECT_DATE_TYPE', 'value'),
        State('STORAGE', 'data'),
    )
    def show_wrong_date(
        n_btn_show_wrong_date, n_interval, date_type, storage_state
    ):
        if (n_btn_show_wrong_date != 0) or (n_interval != 0):
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
                
            if "raw_data" not in table_name_list_exist:
                
                storage_state["raw_data"] = False
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["پایگاه داده خامی موجود نمی‌باشد."],
                    color = 'red',
                    action = "show",
                )
                
                result = [
                    0,
                    True,
                    [],
                    [{}],
                    notify,
                    storage_state
                ]
                
                return result
                
            else:
                
                df = pd.read_sql_query(
                    sql = f"SELECT * FROM raw_data",
                    con = engine
                ).reset_index().rename(columns = {'index':'idx'})
                
                storage_state["raw_data"] = True
                                
                # if "zeros" in action_type:
                    
                #     df.drop(df[df.WATER_TABLE <= 0].index, inplace=True)
                    
                if date_type == "persian_ymd":
                    
                    cols = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
                    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
                    df[cols] = df[cols].astype(pd.Int64Dtype())
                    date_persian, date_gregorian = np.vectorize(chech_persian_date_ymd)(df.YEAR_PERSIAN, df.MONTH_PERSIAN, df.DAY_PERSIAN)
                    df["DATE_PERSIAN"] = list(date_persian)
                    df["DATE_GREGORIAN"] = list(date_gregorian)
                    
                    index_wrong_date = df[df['DATE_GREGORIAN'].isnull()].index.tolist()
                    df_wrong_date = df[df['DATE_GREGORIAN'].isna()]
                    
                    storage_state["index_wrong_date"] = index_wrong_date
                    
                    notify = dmc.Notification(
                        id ="notify",
                        title = "خبر",
                        message = ["جدول تاریخ‌های اشتباه با موفقیت نمایش داده شد."],
                        color = 'green',
                        action = "show",
                    )
                    
                    result = [
                        0,
                        False,
                        df_wrong_date.to_dict('records'),
                        [{"name": i, "id": i, "editable": True if i in cols else False} for i in df_wrong_date.columns[1:]],
                        notify,
                        storage_state
                    ]
                    
                    return result
                
                else:
                    
                    notify = dmc.Notification(
                        id ="notify",
                        title = "",
                        message = [""],
                        color = 'red',
                        action = "hide",
                    )
                            
                    result = [
                        0,
                        True,
                        [],
                        [{}],
                        notify,
                        storage_state
                    ]
                    
                    return result
        else:
            notify = dmc.Notification(
                id ="notify",
                title = "",
                message = [""],
                color = 'red',
                action = "hide",
            )
                    
            result = [
                0,
                True,
                [],
                [{}],
                notify,
                storage_state
            ]
            
            return result
            
