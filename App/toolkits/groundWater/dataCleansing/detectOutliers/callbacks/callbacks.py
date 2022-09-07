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
        if (study_area is not None and len(study_area) != 0) & (aquifer is not None and len(aquifer) != 0) & (well is not None and len(well) != 0) :
            
            try:
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
                    sql = f"SELECT * FROM well WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}'"
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
            except:
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
        Output('BUTTON_SHOW_WRONG_DATE', 'n_clicks'),
        Output('STORAGE', 'data'),
        Output("ALERTS", "children"),
        Input('BUTTON_STAGE_1', 'n_clicks'),
        Input('SELECT_DATE_TYPE', 'value'),        
        State('STORAGE', 'data'),
        State('TABLE_ERROR_DATE', 'data'),
    )
    def modify_wrong_date(
        n_clicks, date_type_value, storage_state, data_table_state
    ):
        if n_clicks != 0:
            
            if storage_state[TABLE_NAME_MODIFIED_DATA]:
                                
                df = pd.read_sql_query(
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA}",
                    con = engine
                ).reset_index().rename(columns = {'index':'idx'})
                
                df = df.drop(storage_state["index_wrong_date"])

                df = pd.concat([df, pd.DataFrame(data_table_state)]).reset_index(drop=True).drop(columns=['idx'])
                
                df.to_sql(
                    name=TABLE_NAME_MODIFIED_DATA,
                    con=engine,
                    if_exists='replace',
                    index=False
                )
                
                storage_state["index_wrong_date"] = []
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خبر",
                    message = ["پایگاه داده با موفقیت بروزرسانی شد."],
                    color = 'green',
                    action = "show",
                )
                        
                result = [
                    0,
                    1,
                    storage_state,
                    notify,
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
                    0,
                    storage_state,
                    notify,
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
                
            if TABLE_NAME_MODIFIED_DATA not in table_name_list_exist:
                
                storage_state[TABLE_NAME_MODIFIED_DATA] = False
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["پایگاه داده اصلاح شده‌ای موجود نمی‌باشد."],
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
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA}",
                    con = engine
                ).reset_index().rename(columns = {'index':'idx'})
                
                storage_state[TABLE_NAME_MODIFIED_DATA] = True
                                
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
                    
                    if len(index_wrong_date) != 0:
                                            
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
                            title = "خبر",
                            message = ["تاریخ اشتباهی در پایگاه داده موجود نمی‌باشد.."],
                            color = 'green',
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
        
    @app.callback(
        Output('BUTTON_DATE', 'n_clicks'),
        Output("ALERTS", "children"),
        Output("STORAGE", "data"),
        Input('BUTTON_DATE', 'n_clicks'),
        Input('SELECT_DATE_TYPE', 'value'),
        State('STORAGE', 'data'),
    )
    def date_complete(
        n, date_type, storage_state
    ):
        if n != 0:
                    
            if len(storage_state["index_wrong_date"]) == 0:
                                
                df = pd.read_sql_query(
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA}",
                    con = engine
                )
                
                if date_type == "persian_ymd":
                    
                    cols_p = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
                    cols_g = ['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']                       
                    df[cols_p] = df[cols_p].apply(pd.to_numeric, errors='coerce')
                    df[cols_p] = df[cols_p].astype(pd.Int64Dtype())
                    date_persian, date_gregorian = np.vectorize(chech_persian_date_ymd)(df.YEAR_PERSIAN, df.MONTH_PERSIAN, df.DAY_PERSIAN)
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
                    
                else:
                    pass
                
                col_sort = ['MAHDOUDE', 'AQUIFER', 'LOCATION', 'DATE_GREGORIAN']                
                df = df.drop_duplicates().sort_values(by=col_sort).reset_index(drop=True)
                
                df.to_sql(
                    name=TABLE_NAME_MODIFIED_DATA,
                    con=engine,
                    if_exists='replace',
                    index=False
                )
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خبر",
                    message = ["تاریخ‌ها به روزرسانی گردید."],
                    color = 'green',
                    action = "show",
                )
                            
                result = [
                    0,
                    notify,
                    storage_state
                ]
                
                return result
            
            else:
                          
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["در پایگاه داده، تاریخ با فرمت اشتباه موجود می‌باشد."],
                    color = 'red',
                    action = "show",
                )
                            
                result = [
                    0,
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
                notify,
                storage_state
            ]
            
            return result


    @app.callback(
        Output("STORAGE", "data"),
        Output("GRAPH", "figure"),
        Output("TABLE", "children"),
        Output("TABLE", "hidden"),
        Output("DIV_TABLE_GRAPH", "hidden"),
        Output("TABLE_GRAPH", "columns"),
        Output("TABLE_GRAPH", "data"),
        Output("BUTTON_SHOW_TABLE_GRAPH", "n_clicks"),
        Input("BUTTON_SHOW_TABLE_GRAPH", "n_clicks"),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        Input('MEAN_METHOD', 'value'),
        Input('DERIVATIVE_METHOD', 'value'),
        State('STORAGE', 'data'),
        State('GRAPH', 'selectedData'),
    )
    def graph(
        n, study_area, aquifer, well, mean, derivation, storage_state, graph_selectedData
    ):
        if (study_area is not None and len(study_area) != 0) & (aquifer is not None and len(aquifer) != 0) & (well is not None and len(well) != 0):
            
            try:
                if (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) != 1):
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" IN {*well,}"
                elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) != 1):
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                elif (len(study_area) != 1) and (len(aquifer) != 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                elif (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) != 1):
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                else:
                    sql = f'SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE ("MAHDOUDE" IN {*study_area,} AND "AQUIFER" IN {*aquifer,} AND "LOCATION" IN {*well,})'
                
                df_m = pd.read_sql_query(
                    sql = sql,
                    con = engine
                )
                
                col_sort = ['MAHDOUDE', 'AQUIFER', 'LOCATION', 'DATE_GREGORIAN']                
                df_modified = df_m.drop_duplicates().sort_values(by=col_sort).reset_index(drop=True).copy()
                
                
                # MEAN METHOD:                
                df_modified["WATER_TABLE_PAD"] = df_modified["WATER_TABLE"].interpolate(method="pad")    
                df_modified["DIFF"] = df_modified["WATER_TABLE_PAD"].diff().abs()
                df_modified["DIFF_MEAN"] = df_modified["DIFF"].rolling(6, min_periods=1).mean().shift(1)
                df_modified["MEAN_METHOD"] = df_modified["DIFF"] > (df_modified["DIFF_MEAN"] * mean)
                
                
                # DERIVATIVE METHOD:
                df_modified["SHIFT_DATE"] = df_modified["DATE_GREGORIAN"].shift(periods=1, fill_value=0)                    
                df_modified[['DATE_GREGORIAN','SHIFT_DATE']] = df_modified[['DATE_GREGORIAN','SHIFT_DATE']].apply(pd.to_datetime)       
                df_modified["DIFF_DATE"] = (df_modified["DATE_GREGORIAN"] - df_modified["SHIFT_DATE"]).dt.days.abs()
                df_modified["DERIVATIV"] = (df_modified["DIFF"] / df_modified["DIFF_DATE"]) * 100
                df_modified["DERIVATIVE_METHOD"] = df_modified["DERIVATIV"] > derivation

                df_modified = df_modified[
                    ["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN", "DATE_PERSIAN", "WATER_TABLE", "MEAN_METHOD", "DERIVATIVE_METHOD", "DESCRIPTION"]
                ]
                
                fig = go.Figure()
                
                for w in well:
                                        
                    df = df_modified[df_modified["LOCATION"] == w]
                    
                    df = df.sort_values(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                    ).reset_index(drop=True)
                    
                    fig.add_trace(
                        go.Scatter(
                            x=df['DATE_GREGORIAN'],
                            y=df['WATER_TABLE'],
                            mode='lines+markers',
                            name=f'داده‌های چاه مشاهده‌ای - {w}',
                            marker=dict(
                                color='blue',
                                size=8,
                            ),
                            line=dict(
                                color='black',
                                width=1
                            )  
                        )
                    )
                    
                    tmp = df[df["MEAN_METHOD"]]
                    
                    fig.add_trace(
                        go.Scatter(
                            x=tmp['DATE_GREGORIAN'],
                            y=tmp['WATER_TABLE'],
                            mode='markers',
                            name=f'روش میانگین',
                            marker=dict(
                                color='green',
                                size=14,
                                symbol='x'
                            )
                        )
                    )
                    
                    tmp = df[df["DERIVATIVE_METHOD"]]
                    
                    fig.add_trace(
                        go.Scatter(
                            x=tmp['DATE_GREGORIAN'],
                            y=tmp['WATER_TABLE'],
                            mode='markers',
                            name=f'روش مشتق',
                            marker=dict(
                                color='orange',
                                size=10,
                                symbol='x'
                            )
                        )
                    )

                fig.update_layout(
                    hoverlabel=dict(
                        namelength = -1
                    ),
                    # hovermode="x unified",
                    # yaxis_title="عمق سطح آب - متر",
                    autosize=False,
                    font=dict(
                        family="Vazir-Regular-FD",
                        size=14,
                        color="RebeccaPurple"
                    ),
                    xaxis=dict(
                        tickformat="%Y-%m-%d",
                    ),
                    title=dict(
                        text='عمق ماهانه سطح آب (متر)',
                        yanchor="top",
                        y=0.98,
                        xanchor="center",
                        x=0.500
                    ),
                    margin=dict(
                        l=50,
                        r=0,
                        b=30,
                        t=50,
                        pad=0
                    ),
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    )
                )
                
                fig.update_xaxes(calendar='jalali')
                
                fig.update_layout(
                    clickmode='event+select',
                    xaxis_title='تاریخ'
                )
                
                if well is not None and len(well) == 1:
                    
                    df_m["DATE_GREGORIAN"] = df_m["DATE_GREGORIAN"].astype(str)
                    
                    title = f"داده‌های سطح ایستابی چاه مشاهده‌ای {well[0]}"
                    
                    content = dash_table.DataTable(
                        columns=[
                            {"name": i, "id": i} for i in df_m.columns
                        ],
                        data=df_m.to_dict('records'),
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        sort_by=[
                            {"column_id": "MAHDOUDE", "direction": "asc"},
                            {"column_id": "AQUIFER", "direction": "asc"},
                            {"column_id": "LOCATION", "direction": "asc"},
                            {"column_id": "DATE_GREGORIAN", "direction": "asc"},
                        ],
                        page_size=14,
                        style_as_list_view=True,
                        style_table={
                            'overflowX': 'auto',
                            'overflowY': 'auto',
                            'direction': 'rtl',
                        },
                        style_cell={
                            'font-family': "Vazir-Regular-FD",
                            'border': '1px solid grey',
                            'font-size': '14px',
                            'text_align': 'center',
                            'minWidth': 150,
                            'maxWidth': 200,
                        },
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'border':'1px solid grey',
                            'fontWeight': 'bold',
                            'text_align': 'center',
                            'height': 'auto',
                        },
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(245, 245, 245)',
                            }
                        ]
                    )
                    
                    if graph_selectedData is None:
                    
                        result = [
                            storage_state,
                            fig,
                            [
                                html.H3(
                                    className="pt-3",
                                    children=title
                                ),
                                content,
                            ],
                            False,
                            True,
                            [{}],
                            [],
                            0
                        ]
                                                
                        return result
                    
                    else:
                        
                        if n != 0:
                            
                            point_selected = pd.DataFrame(graph_selectedData["points"])
                            print(point_selected)
                            point_selected = point_selected[point_selected["curveNumber"] == 0]
                            df_selected = df_m[df_m["DATE_PERSIAN"].isin(point_selected["x"].tolist())]
                            print(df_selected.to_dict('records'))
                            print(df_selected.columns)
                            result = [
                                storage_state,
                                fig,
                                [
                                    html.H3(
                                        className="pt-3",
                                        children=title
                                    ),
                                    content,
                                ],
                                False,
                                False,
                                [{"name": i, "id": i} for i in df_selected.columns],
                                df_selected.to_dict('records'),
                                0
                            ]
                                                    
                            return result
                            
                        else:
                            
                            result = [
                                storage_state,
                                fig,
                                [
                                    html.H3(
                                        className="pt-3",
                                        children=title
                                    ),
                                    content,
                                ],
                                False,
                                True,
                                [{}],
                                [],
                                0
                            ]
                                                    
                            return result
                    
                
                else:
                    
                    result = [
                        storage_state,
                        fig,
                        [],
                        False,
                        True,
                        [{}],
                        [],
                        0
                    ]
                    
                    return result
            
            except:
                
                result = [
                    storage_state,
                    NO_MATCHING_GRAPH_FOUND,
                    [],
                    True,
                    True,
                    [{}],
                    [],
                    0
                ]
                
                return result
            
        else:
            
            result = [
                storage_state,
                NO_MATCHING_GRAPH_FOUND,
                [],
                True,
                True,
                [{}],
                [],
                0
            ]
            
            return result