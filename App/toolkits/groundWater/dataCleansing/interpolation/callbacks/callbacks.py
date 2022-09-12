# import os
# from persiantools.jdatetime import JalaliDate, JalaliDateTime

import json
import itertools
import numpy as np
import pandas as pd
import geopandas as gpd
import psycopg2
import swifter
from dash import no_update
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
from . import *


def toolkits__groundWater__dataCleansing__interpolation__callbacks(app):
    
    # -----------------------------------------------------------------------------
    # SELECT STUDYAREA
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('STUDY_AREA_SELECT', 'options'),
        Input('INTERVAL-STUDYAREA', 'n_intervals'),
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
    
    
    # -----------------------------------------------------------------------------
    # SELECT AQUIFER
    # -----------------------------------------------------------------------------
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
            
            df = df[df["MAHDOUDE"] == study_area_selected]
            
            return [{'label': i, 'value': i} for i in sorted(df.AQUIFER.values)]
        
        else:
            
            return [{}]
    
    
    # -----------------------------------------------------------------------------
    # SELECT WELL
    # -----------------------------------------------------------------------------
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
                
                df = df[df["MAHDOUDE"] == study_area_selected]
                
                df = df[df["AQUIFER"] == aquifer_selected]
                
                return [{'label': i, 'value': i} for i in sorted(df.LOCATION.values)]
            
            else:
                
                return [{}]
        else:
            
            return [{}]
    
    
    # -----------------------------------------------------------------------------
    # UPDATE DROPDOWN LIST
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('STUDY_AREA_SELECT', 'value'),
        Output('AQUIFER_SELECT', 'value'),
        Output('WELL_SELECT', 'value'),
        Output('INTERPOLATE_METHODS', 'value'),
        Output('SAVE_INTERPOLATE_METHODS', 'value'),
        Output('SAVE_WHICH_WELL', 'value'),
        
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
    )
    def update_dropdown_list(
        study_area, aquifer, well
    ):
        if (study_area is not None and len(study_area) != 0) and\
            (aquifer is None or len(aquifer) == 0) and\
                (well is not None and len(well) != 0):
            
            result = [
                no_update,
                [],
                [],
                [],
                None,
                None,
            ]
            
            return result
        
        elif (study_area is None or len(study_area) == 0) and\
            (aquifer is not None and len(aquifer) != 0) and\
                (well is not None and len(well) != 0):
            
            result = [
                [],
                [],
                [],
                [],
                None,
                None,
            ]
            
            return result
        
        else:
            
            result = [
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
                no_update,
            ]
            
            return result


    # -----------------------------------------------------------------------------
    # MAP
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('MAP', 'figure'),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
    )
    def map(
        study_area, aquifer, well
    ):
        if (study_area is not None and len(study_area) != 0) and\
            (aquifer is not None and len(aquifer) != 0) and\
                (well is not None and len(well) != 0) :
            
            try:
                
                # MAHDOUDE
                sql = f"SELECT * FROM mahdoude WHERE \"MAHDOUDE\" = '{study_area}'"
                
                df_study_area = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=engine_layers,
                    geom_col="geometry"
                )
                
                df_study_area_json = json.loads(df_study_area.to_json())
                
                for feature in df_study_area_json["features"]:
                    feature['id'] = feature['properties']['MAHDOUDE']
                
                # AQUIFER            
                sql = f"SELECT * FROM aquifer WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'"
                
                df_aquifer = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=engine_layers,
                    geom_col="geometry"
                )
                
                df_aquifer_json = json.loads(df_aquifer.to_json())
                
                for feature in df_aquifer_json["features"]:
                    feature['id'] = feature['properties']['AQUIFER']
                
                # WELL
                sql = f"SELECT * FROM well WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"
                
                
                df_well = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=engine_layers,
                    geom_col="geometry"
                )
                
                # ALL WELL
                sql = f"SELECT * FROM well WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'"
                
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
                
                fig_tmp = px.choropleth_mapbox(
                    data_frame=df_aquifer,
                    geojson=df_aquifer_json,
                    locations="AQUIFER",
                    hover_name="AQUIFER",
                    hover_data={"MAHDOUDE": True, "AQUIFER": False},
                    opacity=0.7,
                    labels={'MAHDOUDE':'محدوده مطالعاتی', 'AQUIFER':'آبخوان'},                
                )
                
                fig.add_trace(fig_tmp.data[0])
                
                for i, frame in enumerate(fig.frames):
                    fig.frames[i].data += (fig_tmp.frames[i].data[0],)
                
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
    
    # -----------------------------------------------------------------------------
    # SELECT ORDER
    # ----------------------------------------------------------------------------- 
    @app.callback(
        Output('ORDER_INTERPOLATE_METHODS', 'disabled'),
        Input('INTERPOLATE_METHODS', 'value'),
    ) 
    def order_interpolate_methods(
        methods
    ):
        if ("polynomial" in methods) or ("spline" in methods):
            return False
        else:
            return True
    
    # -----------------------------------------------------------------------------
    # CALLBACK: INTERPOLATION
    # -----------------------------------------------------------------------------  
    @app.callback(
        Output('INTERPOLATE_BUTTON', 'n_clicks'),
        Output('GRAPH_INTERPOLATED', 'figure'),
        Output('DIV_GRAPH_INTERPOLATED', 'hidden'),
        Output('DIV_GRAPH', 'hidden'),
        Output("ALERTS", "children"),
        Input('INTERPOLATE_BUTTON', 'n_clicks'),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        Input('INTERPOLATE_METHODS', 'value'),
        Input('ORDER_INTERPOLATE_METHODS', 'value'),
        Input('NUMBER_MONTHS', 'value'),
    ) 
    def interpolation(
        n, study_area, aquifer, well, methods, order, limit
    ):
        if n != 0:
            
            if well is not None and len(well) != 0:
                
                if methods is not None and len(methods) != 0:
                    
                    if len(methods) <= 2:
                        
                        sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"

                        df = pd.read_sql_query(
                            sql = sql,
                            con = engine
                        )
                        
                        if len(methods) == 1:
                            
                            tmp = df.groupby(
                                by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                            ).apply(lambda x: f_interpolate(
                                df=x,
                                method=methods[0],
                                order=order,
                                limit=limit,
                                time_scale="monthly"
                            )).reset_index(drop=True)
                            
                            tmp.sort_values(
                                by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                            ).reset_index(drop=True)
                            
                            fig = go.Figure()
                    
                            fig.add_trace(
                                go.Scatter(
                                    x=tmp['DATE_GREGORIAN'],
                                    y=tmp['WATER_TABLE'],
                                    mode='lines+markers',
                                    name=f"Method: {methods[0]}",
                                    marker=dict(
                                        color='red',
                                        size=10,
                                    ),
                                    line=dict(
                                        color='black',
                                        width=1
                                    )  
                                )
                            )
                            
                            tmp_df = df[~df["WATER_TABLE"].isna()]
                            
                            fig.add_trace(
                                go.Scatter(
                                    x=tmp_df['DATE_GREGORIAN'],
                                    y=tmp_df['WATER_TABLE'],
                                    mode='markers',
                                    name=f'داده‌های کنترل کیفی شده',
                                    marker=dict(
                                        color='blue',
                                        size=12,
                                    )
                                )
                            )
                            
                            fig.update_layout(
                                hoverlabel=dict(
                                    namelength = -1
                                ),
                                yaxis_title="عمق سطح آب - متر",
                                xaxis_title='تاریخ',
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
                                    text=f'عمق ماهانه سطح آب چاه مشاهده‌ای {well} (متر)',
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
                            
                            notify = dmc.Notification(
                                id ="notify",
                                title = "",
                                message = [""],
                                color = 'red',
                                action = "hide",
                            )
                            
                            result = [
                                0,
                                fig,
                                False,
                                True,
                                notify
                            ]
                            
                            return result
                        
                        else:
                            
                            tmp_m0 = df.groupby(
                                by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                            ).apply(lambda x: f_interpolate(
                                df=x,
                                method=methods[0],
                                order=order,
                                limit=limit,
                                time_scale="monthly"
                            )).reset_index(drop=True)
                            
                            tmp_m0.sort_values(
                                by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                            ).reset_index(drop=True)
                            
                            tmp_m1 = df.groupby(
                                by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                            ).apply(lambda x: f_interpolate(
                                df=x,
                                method=methods[1],
                                order=order,
                                limit=limit,
                                time_scale="monthly"
                            )).reset_index(drop=True)
                            
                            tmp_m1.sort_values(
                                by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                            ).reset_index(drop=True)
                            
                            fig = go.Figure()
                    
                            fig.add_trace(
                                go.Scatter(
                                    x=tmp_m0['DATE_GREGORIAN'],
                                    y=tmp_m0['WATER_TABLE'],
                                    mode='lines+markers',
                                    name=f"Method: {methods[0]}",
                                    marker=dict(
                                        color='red',
                                        size=10,
                                    ),
                                    line=dict(
                                        color='black',
                                        width=1
                                    )  
                                )
                            )
                    
                            fig.add_trace(
                                go.Scatter(
                                    x=tmp_m1['DATE_GREGORIAN'],
                                    y=tmp_m1['WATER_TABLE'],
                                    mode='lines+markers',
                                    name=f"Method: {methods[1]}",
                                    marker=dict(
                                        color='orange',
                                        size=10,
                                    ),
                                    line=dict(
                                        color='black',
                                        width=1
                                    )  
                                )
                            )
                            
                            tmp_df = df[~df["WATER_TABLE"].isna()]
                            
                            fig.add_trace(
                                go.Scatter(
                                    x=tmp_df['DATE_GREGORIAN'],
                                    y=tmp_df['WATER_TABLE'],
                                    mode='markers',
                                    name=f'داده‌های کنترل کیفی شده',
                                    marker=dict(
                                        color='blue',
                                        size=12,
                                    ),
                                )
                            )
                            
                            fig.update_layout(
                                hoverlabel=dict(
                                    namelength = -1
                                ),
                                yaxis_title="عمق سطح آب - متر",
                                xaxis_title='تاریخ',
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
                                    text=f'عمق ماهانه سطح آب چاه مشاهده‌ای {well} (متر)',
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
                            
                            notify = dmc.Notification(
                                id ="notify",
                                title = "",
                                message = [""],
                                color = 'red',
                                action = "hide",
                            )
                            
                            result = [
                                0,
                                fig,
                                False,
                                True,
                                notify
                            ]
                            
                            return result
                        
                    else:
                        
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خطا",
                            message = ["برای مقایسه حداکثر دو روش قابل انتخاب است!"],
                            color = 'red',
                            action = "show",
                        )
                        
                        result = [
                            0,
                            NO_MATCHING_GRAPH_FOUND,
                            True,
                            False,
                            notify
                        ]
                        
                        return result
                
                else:
                    
                    notify = dmc.Notification(
                        id ="notify",
                        title = "خطا",
                        message = ["روش درون‌یابی انتخاب نشده است!"],
                        color = 'red',
                        action = "show",
                    )
                    
                    result = [
                        0,
                        NO_MATCHING_GRAPH_FOUND,
                        True,
                        False,
                        notify
                    ]
                    
                    return result
            
            else:
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["چاه مشاهده‌ای انتخاب نشده است!"],
                    color = 'red',
                    action = "show",
                )
                
                result = [
                    0,
                    NO_MATCHING_GRAPH_FOUND,
                    True,
                    False,
                    notify
                ]
                
                return result
            
        else:
            
            notify = dmc.Notification(
                id ="notify",
                title = "",
                message = [""],
                color = 'green',
                action = "hide",
            )
            
            result = [
                0,
                NO_MATCHING_GRAPH_FOUND,
                True,
                False,
                notify
            ]
            
            return result


    # -----------------------------------------------------------------------------
    # CALLBACK: SHOW GRAPH
    # ----------------------------------------------------------------------------- 
    @app.callback(
        Output("GRAPH", "figure"),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
    )
    def show_graph(
        study_area, aquifer, well
    ):
        if study_area is not None and len(study_area) != 0 and\
            aquifer is not None and len(aquifer) != 0 and\
                well is not None and len(well) != 0:
                                        
                    sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"

                    df = pd.read_sql_query(
                        sql = sql,
                        con = engine
                    )
                    
                    col_sort = ['MAHDOUDE', 'AQUIFER', 'LOCATION', 'DATE_GREGORIAN']                    
                    df = df.sort_values(by=col_sort).reset_index(drop=True)
                    
                    fig = go.Figure()
                    
                    fig.add_trace(
                        go.Scatter(
                            x=df['DATE_GREGORIAN'],
                            y=df['WATER_TABLE'],
                            mode='lines+markers',
                            name=f'داده‌های چاه مشاهده‌ای - {well}',
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

                    fig.update_layout(
                        hoverlabel=dict(
                            namelength = -1
                        ),
                        yaxis_title="عمق سطح آب - متر",
                        xaxis_title='تاریخ',
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
                            text=f'عمق ماهانه سطح آب چاه مشاهده‌ای {well} (متر)',
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

                    return fig

        else:
            
            return NO_MATCHING_GRAPH_FOUND


    # -----------------------------------------------------------------------------
    # CALLBACK: OPTION FOR DROPDOWN WHICH-WELL
    # -----------------------------------------------------------------------------  
    @app.callback(
        Output('SAVE_WHICH_WELL', 'options'),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
    ) 
    def which_well_selected(
        study_area, aquifer, well
    ):
        if study_area is not None and len(study_area) != 0 and\
            aquifer is not None and len(aquifer) != 0 and\
                well is not None and len(well) != 0:
                    
                    return [
                        {'label': 'همه چاه‌های مشاهده‌ای', 'value': 0},
                        {'label': f'همه چاه‌های محدوده‌ مطالعاتی {study_area}', 'value': 1},
                        {'label': f'همه چاه‌های آبخوان‌ {aquifer}', 'value': 2},
                        {'label': f'چاه مشاهده‌ای {well}', 'value': 3},
                    ]
                    
        elif study_area is not None and len(study_area) != 0 and\
            aquifer is not None and len(aquifer) != 0:
            
                return [
                    {'label': 'همه چاه‌های مشاهده‌ای', 'value': 0},
                    {'label': f'همه چاه‌های محدوده‌ مطالعاتی {study_area}', 'value': 1},
                    {'label': f'همه چاه‌های آبخوان‌ {aquifer}', 'value': 2},
                ]
                
        elif study_area is not None and len(study_area) != 0:
            
                return [
                    {'label': 'همه چاه‌های مشاهده‌ای', 'value': 0},
                    {'label': f'همه چاه‌های محدوده‌ مطالعاتی {study_area}', 'value': 1},
                ]
                
        else:
            
            return [
                {'label': 'همه چاه‌های مشاهده‌ای', 'value': 0},
            ]


    # -----------------------------------------------------------------------------
    # CALLBACK: SAVE INTERPOLATED DATA
    # -----------------------------------------------------------------------------  
    @app.callback(
        Output('SAVE_INTERPOLATE_BUTTON', 'n_clicks'),
        Output("ALERTS", "children"),
        Input('SAVE_INTERPOLATE_BUTTON', 'n_clicks'),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        Input('SAVE_INTERPOLATE_METHODS', 'value'),
        Input('SAVE_ORDER_INTERPOLATE_METHODS', 'value'),
        Input('SAVE_NUMBER_MONTHS', 'value'),
        Input('SAVE_WHICH_WELL', 'value'),
    ) 
    def save_interpolation(
        n, study_area, aquifer, well, method, order, limit, which_well
    ):
        if n != 0:
            
            if method is not None and len(method) != 0:
                
                table_exist = find_table(
                    database=POSTGRES_DB_NAME,
                    table=TABLE_NAME_INTERPOLATED_DATA,
                    user=POSTGRES_USER_NAME,
                    password=POSTGRES_PASSWORD,
                    host=POSTGRES_HOST,
                    port=POSTGRES_PORT
                )
                
                if which_well is not None:
                    
                    if which_well == 0:

                        sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA}"

                        df = pd.read_sql_query(
                            sql = sql,
                            con = engine
                        )
                                                
                        df = df.groupby(
                            by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                        ).apply(lambda x: f_interpolate(
                            df=x,
                            method=method,
                            order=order,
                            limit=limit,
                            time_scale="monthly"
                        )).reset_index(drop=True)
                        
                        df = df.sort_values(
                            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                        )
                        
                        update_table(
                            data=df,
                            table_exist=table_exist,
                            table_name=TABLE_NAME_INTERPOLATED_DATA,
                            engine=engine,
                            study_area=None,
                            aquifer=None,
                            well=None,
                        )
                        
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خبر",
                            message = ["تغییرات با موفقیت آپدیت شد!"],
                            color = 'green',
                            action = "show",
                        )
                        
                        result = [
                            0,
                            notify
                        ]
                    
                        return result
                    
                    elif which_well == 1:
                        
                        sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area}'"

                        df = pd.read_sql_query(
                            sql = sql,
                            con = engine
                        )
                        
                        df = df.groupby(
                            by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                        ).apply(lambda x: f_interpolate(
                            df=x,
                            method=method,
                            order=order,
                            limit=limit,
                            time_scale="monthly"
                        )).reset_index(drop=True)
                        
                        df = df.sort_values(
                            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                        )
                                            
                        update_table(
                            data=df,
                            table_exist=table_exist,
                            table_name=TABLE_NAME_INTERPOLATED_DATA,
                            engine=engine,
                            study_area=study_area,
                            aquifer=None,
                            well=None,
                        )
                        
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خبر",
                            message = ["تغییرات با موفقیت آپدیت شد!"],
                            color = 'green',
                            action = "show",
                        )
                        
                        result = [
                            0,
                            notify
                        ]
                    
                        return result
                    
                    elif which_well == 2:
                        
                        sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'"

                        df = pd.read_sql_query(
                            sql = sql,
                            con = engine
                        )
                                                
                        df = df.groupby(
                            by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                        ).apply(lambda x: f_interpolate(
                            df=x,
                            method=method,
                            order=order,
                            limit=limit,
                            time_scale="monthly"
                        )).reset_index(drop=True)
                        
                        df = df.sort_values(
                            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                        )
                                                
                        update_table(
                            data=df,
                            table_exist=table_exist,
                            table_name=TABLE_NAME_INTERPOLATED_DATA,
                            engine=engine,
                            study_area=study_area,
                            aquifer=aquifer,
                            well=None,
                        )
                        
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خبر",
                            message = ["تغییرات با موفقیت آپدیت شد!"],
                            color = 'green',
                            action = "show",
                        )
                        
                        result = [
                            0,
                            notify
                        ]
                    
                        return result
                    
                    elif which_well == 3:
                        
                        sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"

                        df = pd.read_sql_query(
                            sql = sql,
                            con = engine
                        )
                                                
                        df = df.groupby(
                            by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                        ).apply(lambda x: f_interpolate(
                            df=x,
                            method=method,
                            order=order,
                            limit=limit,
                            time_scale="monthly"
                        )).reset_index(drop=True)
                        
                        df = df.sort_values(
                            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                        )
                                                
                        update_table(
                            data=df,
                            table_exist=table_exist,
                            table_name=TABLE_NAME_INTERPOLATED_DATA,
                            engine=engine,
                            study_area=study_area,
                            aquifer=aquifer,
                            well=well,
                        )
                        
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خبر",
                            message = ["تغییرات با موفقیت آپدیت شد!"],
                            color = 'green',
                            action = "show",
                        )
                        
                        result = [
                            0,
                            notify
                        ]
                    
                        return result
                    
                    else:
                        
                        pass
                
                else:
                    
                    notify = dmc.Notification(
                        id ="notify",
                        title = "خطا",
                        message = ["محدوده اعمال تغییرات انتخاب نشده است!"],
                        color = 'red',
                        action = "show",
                    )
                    
                    result = [
                        0,
                        notify
                    ]
                    
                    return result
            
            else:
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["روش درون‌یابی انتخاب نشده است!"],
                    color = 'red',
                    action = "show",
                )
                
                result = [
                    0,
                    notify
                ]
                
                return result
        
        else:
            
            notify = dmc.Notification(
                id ="notify",
                title = "",
                message = [""],
                color = 'green',
                action = "hide",
            )
            
            result = [
                0,
                notify
            ]
            
            return result








    
    
    

    
    
    
    # @app.callback(
    #     Output('BUTTON_STAGE_1', 'n_clicks'),
    #     Output('BUTTON_SHOW_WRONG_DATE', 'n_clicks'),
    #     Output('STORAGE', 'data'),
    #     Output("ALERTS", "children"),
    #     Input('BUTTON_STAGE_1', 'n_clicks'),
    #     Input('SELECT_DATE_TYPE', 'value'),        
    #     State('STORAGE', 'data'),
    #     State('TABLE_ERROR_DATE', 'data'),
    # )
    # def modify_wrong_date(
    #     n_clicks, date_type_value, storage_state, data_table_state
    # ):
    #     if n_clicks != 0:
            
    #         if storage_state[TABLE_NAME_MODIFIED_DATA]:
                
    #             df_selected_modify = pd.DataFrame(data_table_state)
                
    #             df_selected_modify["DESCRIPTION"] = df_selected_modify["DESCRIPTION"] + "تاریخ اصلاح شده است."
                                
    #             df = pd.read_sql_query(
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA}",
    #                 con = engine
    #             ).reset_index().rename(columns = {'index':'idx'})
                
    #             df = df.drop(storage_state["index_wrong_date"])

    #             df = pd.concat([df, df_selected_modify]).reset_index(drop=True).drop(columns=['idx'])
                
    #             df["DATE_GREGORIAN"] = df["DATE_GREGORIAN"].apply(pd.to_datetime)
                
    #             df['WATER_TABLE'] = df['WATER_TABLE'].astype('float64')
                
    #             df.to_sql(
    #                 name=TABLE_NAME_MODIFIED_DATA,
    #                 con=engine,
    #                 if_exists='replace',
    #                 index=False
    #             )
                
    #             storage_state["index_wrong_date"] = []
                
    #             notify = dmc.Notification(
    #                 id ="notify",
    #                 title = "خبر",
    #                 message = ["پایگاه داده با موفقیت بروزرسانی شد."],
    #                 color = 'green',
    #                 action = "show",
    #             )
                        
    #             result = [
    #                 0,
    #                 1,
    #                 storage_state,
    #                 notify,
    #             ]
                
    #             return result
            
    #         else:
                
    #             notify = dmc.Notification(
    #                 id ="notify",
    #                 title = "",
    #                 message = [""],
    #                 color = 'red',
    #                 action = "hide",
    #             )
                        
    #             result = [
    #                 0,
    #                 0,
    #                 storage_state,
    #                 notify,
    #             ]
                
    #             return result
        
    #     else:
            
    #         notify = dmc.Notification(
    #             id ="notify",
    #             title = "",
    #             message = [""],
    #             color = 'red',
    #             action = "hide",
    #         )
                    
    #         result = [
    #             0,
    #             0,
    #             storage_state,
    #             notify,
    #         ]
            
    #         return result
            


    # @app.callback(
    #     Output('BUTTON_SHOW_WRONG_DATE', 'n_clicks'),
    #     Output('DIV_TABLE_ERROR_DATE', 'hidden'),
    #     Output('TABLE_ERROR_DATE', 'data'),
    #     Output('TABLE_ERROR_DATE', 'columns'),
    #     Output("ALERTS", "children"),
    #     Output("STORAGE", "data"),
    #     Input('BUTTON_SHOW_WRONG_DATE', 'n_clicks'),
    #     Input('SELECT_DATE_TYPE', 'value'),
    #     State('STORAGE', 'data'),
    # )
    # def show_wrong_date(
    #     n_btn_show_wrong_date, date_type, storage_state
    # ):
    #     if (n_btn_show_wrong_date != 0):
    #         conn = psycopg2.connect(
    #             database=POSTGRES_DB_NAME,
    #             user=POSTGRES_USER_NAME,
    #             password=POSTGRES_PASSWORD,
    #             host=POSTGRES_HOST,
    #             port=POSTGRES_PORT
    #         )    
    #         conn.autocommit = True    
    #         cursor = conn.cursor()    
    #         sql = '''SELECT table_name FROM information_schema.tables;'''
    #         cursor.execute(sql)
    #         table_name_list_exist = list(itertools.chain.from_iterable(cursor.fetchall()))
    #         conn.close()
                
    #         if TABLE_NAME_MODIFIED_DATA not in table_name_list_exist:
                
    #             storage_state[TABLE_NAME_MODIFIED_DATA] = False
                
    #             notify = dmc.Notification(
    #                 id ="notify",
    #                 title = "خطا",
    #                 message = ["پایگاه داده اصلاح شده‌ای موجود نمی‌باشد."],
    #                 color = 'red',
    #                 action = "show",
    #             )
                
    #             result = [
    #                 0,
    #                 True,
    #                 [],
    #                 [{}],
    #                 notify,
    #                 storage_state
    #             ]
                
    #             return result
                
    #         else:
                
    #             df = pd.read_sql_query(
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA}",
    #                 con = engine
    #             ).reset_index().rename(columns = {'index':'idx'})
                
    #             storage_state[TABLE_NAME_MODIFIED_DATA] = True
                                
    #             # if "zeros" in action_type:
                    
    #             #     df.drop(df[df.WATER_TABLE <= 0].index, inplace=True)
                    
    #             if date_type == "persian_ymd":
                    
    #                 cols = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
    #                 df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    #                 df[cols] = df[cols].astype(pd.Int64Dtype())
    #                 date_persian, date_gregorian = np.vectorize(check_persian_date_ymd)(df.YEAR_PERSIAN, df.MONTH_PERSIAN, df.DAY_PERSIAN)
    #                 df["DATE_PERSIAN"] = list(date_persian)
    #                 df["DATE_GREGORIAN"] = list(date_gregorian)
                    
    #                 index_wrong_date = df[df['DATE_GREGORIAN'].isnull()].index.tolist()
    #                 df_wrong_date = df[df['DATE_GREGORIAN'].isna()]
                    
    #                 storage_state["index_wrong_date"] = index_wrong_date
                    
    #                 if len(index_wrong_date) != 0:
                                            
    #                     notify = dmc.Notification(
    #                         id ="notify",
    #                         title = "خبر",
    #                         message = ["جدول تاریخ‌های اشتباه با موفقیت نمایش داده شد."],
    #                         color = 'green',
    #                         action = "show",
    #                     )
                                            
    #                     result = [
    #                         0,
    #                         False,
    #                         df_wrong_date.to_dict('records'),
    #                         [{"name": i, "id": i, "editable": True if i in cols else False} for i in df_wrong_date.columns[1:]],
    #                         notify,
    #                         storage_state
    #                     ]
                        
    #                     return result
                    
    #                 else:
                        
    #                     notify = dmc.Notification(
    #                         id ="notify",
    #                         title = "خبر",
    #                         message = ["تاریخ اشتباهی در پایگاه داده موجود نمی‌باشد.."],
    #                         color = 'green',
    #                         action = "show",
    #                     )
                                            
    #                     result = [
    #                         0,
    #                         True,
    #                         [],
    #                         [{}],
    #                         notify,
    #                         storage_state
    #                     ]
                        
    #                     return result
                
    #             else:
                    
    #                 notify = dmc.Notification(
    #                     id ="notify",
    #                     title = "",
    #                     message = [""],
    #                     color = 'red',
    #                     action = "hide",
    #                 )
                            
    #                 result = [
    #                     0,
    #                     True,
    #                     [],
    #                     [{}],
    #                     notify,
    #                     storage_state
    #                 ]
                    
    #                 return result
    #     else:
    #         notify = dmc.Notification(
    #             id ="notify",
    #             title = "",
    #             message = [""],
    #             color = 'red',
    #             action = "hide",
    #         )
                    
    #         result = [
    #             0,
    #             True,
    #             [],
    #             [{}],
    #             notify,
    #             storage_state
    #         ]
            
    #         return result



    # @app.callback(
    #     Output('BUTTON_DATE', 'n_clicks'),
    #     Output("ALERTS", "children"),
    #     Output("STORAGE", "data"),
    #     Input('BUTTON_DATE', 'n_clicks'),
    #     Input('SELECT_DATE_TYPE', 'value'),
    #     State('STORAGE', 'data'),
    # )
    # def date_complete(
    #     n, date_type, storage_state
    # ):
    #     if n != 0:
                    
    #         if len(storage_state["index_wrong_date"]) == 0:
                                
    #             df = pd.read_sql_query(
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA}",
    #                 con = engine
    #             )
                
    #             if date_type == "persian_ymd":
                    
    #                 cols_p = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
    #                 cols_g = ['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']                       
    #                 df[cols_p] = df[cols_p].apply(pd.to_numeric, errors='coerce')
    #                 df[cols_p] = df[cols_p].astype(pd.Int64Dtype())
    #                 date_persian, date_gregorian = np.vectorize(check_persian_date_ymd)(df.YEAR_PERSIAN, df.MONTH_PERSIAN, df.DAY_PERSIAN)
    #                 df["DATE_PERSIAN"] = list(date_persian)
    #                 df["DATE_GREGORIAN"] = list(date_gregorian)
    #                 df[cols_p] = df['DATE_PERSIAN'].str.split('-', 2, expand=True)
    #                 df[cols_g] = df['DATE_GREGORIAN'].astype(str).str.split('-', 2, expand=True)
    #                 df["YEAR_PERSIAN"] = df["YEAR_PERSIAN"].astype(str).str.zfill(4)
    #                 df["MONTH_PERSIAN"] = df["MONTH_PERSIAN"].astype(str).str.zfill(2)
    #                 df["DAY_PERSIAN"] = df["DAY_PERSIAN"].astype(str).str.zfill(2)
    #                 df["YEAR_GREGORIAN"] = df["YEAR_GREGORIAN"].str.zfill(4)
    #                 df["MONTH_GREGORIAN"] = df["MONTH_GREGORIAN"].str.zfill(2)
    #                 df["DAY_GREGORIAN"] = df["DAY_GREGORIAN"].str.zfill(2)
    #                 df['DATE_PERSIAN'] = df["YEAR_PERSIAN"] + "-" + df["MONTH_PERSIAN"] + "-" + df["DAY_PERSIAN"]
    #                 df['DATE_GREGORIAN'] = df["YEAR_GREGORIAN"] + "-" + df["MONTH_GREGORIAN"] + "-" + df["DAY_GREGORIAN"]
    #                 df["DATE_GREGORIAN"] = df["DATE_GREGORIAN"].apply(pd.to_datetime)
                    
    #             else:
    #                 pass
                
    #             col_sort = ['MAHDOUDE', 'AQUIFER', 'LOCATION', 'DATE_GREGORIAN']                
    #             df = df.drop_duplicates().sort_values(by=col_sort).reset_index(drop=True)
                
    #             df.to_sql(
    #                 name=TABLE_NAME_MODIFIED_DATA,
    #                 con=engine,
    #                 if_exists='replace',
    #                 index=False
    #             )
                
    #             notify = dmc.Notification(
    #                 id ="notify",
    #                 title = "خبر",
    #                 message = ["تاریخ‌ها به روزرسانی گردید."],
    #                 color = 'green',
    #                 action = "show",
    #             )
                            
    #             result = [
    #                 0,
    #                 notify,
    #                 storage_state
    #             ]
                
    #             return result
            
    #         else:
                          
    #             notify = dmc.Notification(
    #                 id ="notify",
    #                 title = "خطا",
    #                 message = ["در پایگاه داده، تاریخ با فرمت اشتباه موجود می‌باشد."],
    #                 color = 'red',
    #                 action = "show",
    #             )
                            
    #             result = [
    #                 0,
    #                 notify,
    #                 storage_state
    #             ]
                
    #             return result
        
    #     else:
            
    #         notify = dmc.Notification(
    #             id ="notify",
    #             title = "",
    #             message = [""],
    #             color = 'red',
    #             action = "hide",
    #         )
                        
    #         result = [
    #             0,
    #             notify,
    #             storage_state
    #         ]
            
    #         return result


    
    
    
    
    # @app.callback(
    #     Output("DIV_TABLE", "children"),        
    #     Input('STUDY_AREA_SELECT', 'value'),
    #     Input('AQUIFER_SELECT', 'value'),
    #     Input('WELL_SELECT', 'value'),
    # )
    # def show_table(
    #     study_area, aquifer, well
    # ):
    #     if study_area is not None and len(study_area) != 0 and\
    #         aquifer is not None and len(aquifer) != 0 and\
    #             well is not None and len(well) != 0:
                    
    #                 try:
                
    #                     if (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) == 1):
    #                         sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
    #                     elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) != 1):
    #                         sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" IN {*well,}"
    #                     elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) != 1):
    #                         sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
    #                     elif (len(study_area) != 1) and (len(aquifer) != 1) and (len(well) == 1):
    #                         sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
    #                     elif (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) != 1):
    #                         sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
    #                     elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) == 1):
    #                         sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
    #                     elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) == 1):
    #                         sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
    #                     else:
    #                         sql = f'SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE ("MAHDOUDE" IN {*study_area,} AND "AQUIFER" IN {*aquifer,} AND "LOCATION" IN {*well,})'
                    
    #                     df_m = pd.read_sql_query(
    #                         sql = sql,
    #                         con = engine
    #                     )
                        
    #                     df_m["DATE_GREGORIAN"] = df_m["DATE_GREGORIAN"].dt.strftime('%Y-%m-%d')
                        
    #                     if well is not None and len(well) == 1:
                            
    #                         table = dash_table.DataTable(
    #                             id="TABLE",
    #                             data=df_m.to_dict('records'),
    #                             columns=[{"name": i, "id": i} for i in df_m.columns],
    #                             filter_action="native",
    #                             sort_action="native",
    #                             sort_mode="multi",
    #                             sort_by=[
    #                                 {"column_id": "MAHDOUDE", "direction": "asc"},
    #                                 {"column_id": "AQUIFER", "direction": "asc"},
    #                                 {"column_id": "LOCATION", "direction": "asc"},
    #                                 {"column_id": "DATE_GREGORIAN", "direction": "asc"},
    #                             ],
    #                             page_size=14,
    #                             style_as_list_view=True,
    #                             style_table={
    #                                 'overflowX': 'auto',
    #                                 'overflowY': 'auto',
    #                                 'direction': 'rtl',
    #                             },
    #                             style_cell={
    #                                 'font-family': "Vazir-Regular-FD",
    #                                 'border': '1px solid grey',
    #                                 'font-size': '14px',
    #                                 'text_align': 'center',
    #                                 'minWidth': 150,
    #                                 'maxWidth': 200,
    #                             },
    #                             style_header={
    #                                 'backgroundColor': 'rgb(210, 210, 210)',
    #                                 'border':'1px solid grey',
    #                                 'fontWeight': 'bold',
    #                                 'text_align': 'center',
    #                                 'height': 'auto',
    #                             },
    #                             style_data={
    #                                 'color': 'black',
    #                                 'backgroundColor': 'white'
    #                             },
    #                             style_data_conditional=[
    #                                 {
    #                                     'if': {'row_index': 'odd'},
    #                                     'backgroundColor': 'rgb(245, 245, 245)',
    #                                 }
    #                             ]
    #                         )   
                            
    #                         return [
    #                             html.H3(
    #                                 className="pt-3",
    #                                 children=f"داده‌های سطح ایستابی چاه مشاهده‌ای {well[0]}"
    #                             ),
    #                             table,
    #                         ]
                            
    #                     else:
    #                         return []
                    
    #                 except:
    #                     return []
    #     else:
    #         return []
    
    
    
    # @app.callback(
    #     Output("DIV_TABLE_SELECTED_DATA", "hidden"),
    #     Output("DIV_TABLE_SELECTED_DATA", "children"),
    #     Output('STORAGE', 'data'),
    #     Input("GRAPH", "selectedData"),
    #     Input('STUDY_AREA_SELECT', 'value'),
    #     Input('AQUIFER_SELECT', 'value'),
    #     Input('WELL_SELECT', 'value'),
    #     State('STORAGE', 'data'),
    # )
    # def show_table_selected_data(
    #     selectedData, study_area, aquifer, well, storage_state
    # ):
    #     if well is not None and len(well) == 1:
    #         if selectedData is not None:
    #             if (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) == 1):
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
    #             elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) != 1):
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" IN {*well,}"
    #             elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) != 1):
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
    #             elif (len(study_area) != 1) and (len(aquifer) != 1) and (len(well) == 1):
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
    #             elif (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) != 1):
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
    #             elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) == 1):
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
    #             elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) == 1):
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
    #             else:
    #                 sql = f'SELECT * FROM {TABLE_NAME_MODIFIED_DATA} WHERE ("MAHDOUDE" IN {*study_area,} AND "AQUIFER" IN {*aquifer,} AND "LOCATION" IN {*well,})'
            
    #             df = pd.read_sql_query(
    #                 sql = sql,
    #                 con = engine
    #             )
                
    #             if len(selectedData["points"]) != 0:
                    
    #                 point_selected = pd.DataFrame(selectedData["points"])
    #                 point_selected = point_selected[point_selected["curveNumber"] == 0]
    #                 df_selected = df[df["DATE_PERSIAN"].isin(point_selected["x"].tolist())]
                                        
    #                 df_table_database = pd.read_sql_query(
    #                     sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA}",
    #                     con = engine
    #                 )
                    
    #                 ind = df_table_database.MAHDOUDE.isin(df_selected.MAHDOUDE) &\
    #                     df_table_database.AQUIFER.isin(df_selected.AQUIFER) &\
    #                         df_table_database.LOCATION.isin(df_selected.LOCATION) &\
    #                             df_table_database.DATE_PERSIAN.isin(df_selected.DATE_PERSIAN)
                                
    #                 ind = df_table_database[ind].index.tolist()
                    
    #                 storage_state["index_selected_data"] = ind
                    
    #                 df_selected["DATE_GREGORIAN"] = df_selected["DATE_GREGORIAN"].dt.strftime('%Y-%m-%d')
                    
    #                 table_selected_data = dash_table.DataTable(
    #                     id="TABLE_SELECTED_DATA",
    #                     columns=[{"name": i, "id": i, "editable": True if i == "WATER_TABLE" else False} for i in df_selected.columns],
    #                     data=df_selected.to_dict("records"),
    #                     editable=True,
    #                     row_deletable=True,
    #                     page_size=12,
    #                     style_as_list_view=True,
    #                     style_table={
    #                         'overflowX': 'auto',
    #                         'overflowY': 'auto',
    #                         'direction': 'rtl',
    #                     },
    #                     style_cell={
    #                         'font-family': "Vazir-Regular-FD",
    #                         'border': '1px solid grey',
    #                         'font-size': '14px',
    #                         'text_align': 'center',
    #                         'minWidth': 150,
    #                         'maxWidth': 200,
    #                     },
    #                     style_header={
    #                         'backgroundColor': 'rgb(210, 210, 210)',
    #                         'border':'1px solid grey',
    #                         'fontWeight': 'bold',
    #                         'text_align': 'center',
    #                         'height': 'auto',
    #                     },
    #                     style_data={
    #                         'color': 'black',
    #                         'backgroundColor': 'white'
    #                     },
    #                     style_data_conditional=[
    #                         {
    #                             'if': {'row_index': 'odd'},
    #                             'backgroundColor': 'rgb(245, 245, 245)',
    #                         }
    #                     ]
    #                 )
                    
    #                 result = [
    #                     False,
    #                     [
    #                         html.H3(
    #                             className="pt-3",
    #                             children="جدول داده‌های انتخاب شده از نمودار"
    #                         ),
    #                         table_selected_data,
    #                     ],
    #                     storage_state
    #                 ]
    #                 return result
    #             else:
    #                 storage_state["index_selected_data"] = []
    #                 result = [
    #                     True,
    #                     None,
    #                     storage_state
    #                 ]
    #                 return result
    #         else:
    #             storage_state["index_selected_data"] = []
    #             result = [
    #                 True,
    #                 None,
    #                 storage_state
    #             ]
    #             return result
    #     else:
    #         storage_state["index_selected_data"] = []
    #         result = [
    #             True,
    #             None,
    #             storage_state
    #         ]
    #         return result
    
    
    # @app.callback(
    #     Output("BUTTON_TABLE_GRAPH", "n_clicks"),
    #     Output("ALERTS", "children"),
    #     Output('STORAGE', 'data'),
    #     Input("BUTTON_TABLE_GRAPH", "n_clicks"),
    #     State("TABLE_SELECTED_DATA", "data"),
    #     State('STORAGE', 'data'),
    # )
    # def modify_selected_data(
    #     n_clicks, table_selected_data_state, storage_state
    # ):
    #     if n_clicks != 0:
            
    #         if len(storage_state["index_selected_data"]) != 0:
                
    #             df_selected_data = pd.DataFrame(table_selected_data_state)
    #             df_selected_data["DESCRIPTION"] = df_selected_data["DESCRIPTION"] + "سطح ایستابی اصلاح شده است."
                                
    #             df = pd.read_sql_query(
    #                 sql = f"SELECT * FROM {TABLE_NAME_MODIFIED_DATA}",
    #                 con = engine
    #             )
                
    #             df = df.drop(storage_state["index_selected_data"])
                
    #             df = pd.concat([df, df_selected_data]).reset_index(drop=True)
                
    #             df['WATER_TABLE'] = df['WATER_TABLE'].astype('float64')
                
    #             df["DATE_GREGORIAN"] = df["DATE_GREGORIAN"].apply(pd.to_datetime)
                
    #             df.to_sql(
    #                 name=TABLE_NAME_MODIFIED_DATA,
    #                 con=engine,
    #                 if_exists='replace',
    #                 index=False
    #             )
                
    #             storage_state["index_selected_data"] = []
                
    #             notify = dmc.Notification(
    #                 id ="notify",
    #                 title = "خبر",
    #                 message = ["پایگاه داده با موفقیت بروزرسانی شد."],
    #                 color = 'green',
    #                 action = "show",
    #             )
                        
    #             result = [
    #                 0,
    #                 storage_state,
    #                 notify,
    #             ]
                
    #             return result
            
    #         else:
                
    #             notify = dmc.Notification(
    #                 id ="notify",
    #                 title = "",
    #                 message = [""],
    #                 color = 'red',
    #                 action = "hide",
    #             )
                        
    #             result = [
    #                 0,
    #                 storage_state,
    #                 notify
    #             ]
                
    #             return result
        
    #     else:
            
    #         notify = dmc.Notification(
    #             id ="notify",
    #             title = "",
    #             message = [""],
    #             color = 'red',
    #             action = "hide",
    #         )
                    
    #         result = [
    #             0,
    #             storage_state,
    #             notify
    #         ]
            
    #         return result