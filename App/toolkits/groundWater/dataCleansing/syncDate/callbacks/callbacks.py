import json
import itertools
import tempfile
import numpy as np
import pandas as pd
import geopandas as gpd
import psycopg2
from dash import no_update, dcc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
from . import *


def toolkits__groundWater__dataCleansing__syncDate__callbacks(app):
    
    # -----------------------------------------------------------------------------
    # CALLBACK: SELECT STUDYAREA
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('STUDY_AREA_SELECT', 'options'),
        Input('INTERVAL-STUDYAREA', 'n_intervals'),
    )
    def study_area_select(
        n
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
        
        if "geoinfo" in table_name_list_exist:
            
            df = pd.read_sql_query(
                sql='SELECT DISTINCT "MAHDOUDE" FROM geoinfo;',
                con=ENGINE_DATA
            )
        
            return [{'label': i, 'value': i} for i in sorted(df.MAHDOUDE.values)]
        
        else:
            
            return [{}]
    
    
    # -----------------------------------------------------------------------------
    # # CALLBACK: SELECT AQUIFER
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
                con=ENGINE_DATA
            )
            
            df = df[df["MAHDOUDE"] == study_area_selected]
            
            return [{'label': i, 'value': i} for i in sorted(df.AQUIFER.values)]
        
        else:
            
            return [{}]
    
    
    # -----------------------------------------------------------------------------
    # # CALLBACK: SELECT WELL
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
                    con=ENGINE_DATA
                )
                
                df = df[df["MAHDOUDE"] == study_area_selected]
                
                df = df[df["AQUIFER"] == aquifer_selected]
                
                return [{'label': i, 'value': i} for i in sorted(df.LOCATION.values)]
            
            else:
                
                return [{}]
        else:
            
            return [{}]
    
    
    # -----------------------------------------------------------------------------
    # # CALLBACK: UPDATE DROPDOWN LIST
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('STUDY_AREA_SELECT', 'value'),
        Output('AQUIFER_SELECT', 'value'),
        Output('WELL_SELECT', 'value'),        
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
            ]
            
            return result
        
        elif (study_area is None or len(study_area) == 0) and\
            (aquifer is not None and len(aquifer) != 0) and\
                (well is not None and len(well) != 0):
            
            result = [
                [],
                [],
                [],
            ]
            
            return result
        
        else:
            
            result = [
                no_update,
                no_update,
                no_update,
            ]
            
            return result


    # -----------------------------------------------------------------------------
    # # CALLBACK: MAP
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
                sql = f"SELECT * FROM {DB_LAYERS_TABLE_MAHDOUDE} WHERE \"MAHDOUDE\" = '{study_area}'"
                
                df_study_area = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=ENGINE_LAYERS,
                    geom_col="geometry"
                )
                
                df_study_area_json = json.loads(df_study_area.to_json())
                
                for feature in df_study_area_json["features"]:
                    feature['id'] = feature['properties']['MAHDOUDE']
                
                # AQUIFER            
                sql = f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'"
                
                df_aquifer = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=ENGINE_LAYERS,
                    geom_col="geometry"
                )
                
                df_aquifer_json = json.loads(df_aquifer.to_json())
                
                for feature in df_aquifer_json["features"]:
                    feature['id'] = feature['properties']['AQUIFER']
                
                # WELL
                sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"
                
                
                df_well = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=ENGINE_LAYERS,
                    geom_col="geometry"
                )
                
                # ALL WELL
                sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'"
                
                df_all_well = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=ENGINE_LAYERS,
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
    # CALLBACK: SYNC DATE
    # -----------------------------------------------------------------------------  
    @app.callback(
        Output('SYNC_DATE_BUTTON', 'n_clicks'),
        Output('GRAPH_SYNCHRONIZED', 'figure'),
        Output('DIV_GRAPH_SYNCHRONIZED', 'hidden'),
        Output('DIV_GRAPH', 'hidden'),
        Output("ALERTS", "children"),
        
        Input('SYNC_DATE_BUTTON', 'n_clicks'),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        Input('SYNC_DAY', 'value'),
    ) 
    def sync_date(
        n, study_area, aquifer, well, day,
    ):
        if n != 0:
            
            if well is not None and len(well) != 0:
                
                sql = f"SELECT * FROM {DB_DATA_TABLE_INTERPOLATEDDATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"

                df = pd.read_sql_query(
                    sql = sql,
                    con = ENGINE_DATA
                )
                
                if len(df) == 0:
                
                    notify = dmc.Notification(
                        id ="notify",
                        title = "خطا",
                        message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای یا محدوده مطالعاتی انجام دهید."],
                        color = 'red',
                        action = "show",
                        autoClose=10000
                    )
                    
                    result = [
                        0,
                        NO_MATCHING_GRAPH_FOUND,
                        True,
                        False,
                        notify
                    ]
                    
                    return result

                tmp = df.groupby(
                    by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                ).apply(lambda x: f_syncdate(
                    df=x,
                    day=day
                )).reset_index(drop=True)
                            
                tmp.sort_values(
                    by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                ).reset_index(drop=True)
                
                fig = go.Figure()
        
                fig.add_trace(
                    go.Scatter(
                        x=df['DATE_GREGORIAN'],
                        y=df['WATER_TABLE'],
                        mode='lines+markers',
                        name=f'داده‌های کنترل کیفی شده',
                        marker=dict(
                            color='blue',
                            size=10,
                        ),
                        line=dict(
                            color='black',
                            width=0.5
                        )  
                    )
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=tmp['DATE_GREGORIAN'],
                        y=tmp['WATER_TABLE'],
                        mode='lines+markers',
                        name=f'داده‌های هماهنگ‌سازی شده تاریخ برای روز {day}ام',
                        marker=dict(
                            color='black',
                            size=10,
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
        Output("ALERTS", "children"),
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
                                        
                    sql = f"SELECT * FROM {DB_DATA_TABLE_INTERPOLATEDDATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"

                    df = pd.read_sql_query(
                        sql = sql,
                        con = ENGINE_DATA
                    )
                                        
                    if len(df) == 0:
                        
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خطا",
                            message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای یا محدوده مطالعاتی انجام دهید."],
                            color = 'red',
                            action = "show",
                            autoClose=10000
                        )
                        
                        result = [
                            NO_MATCHING_GRAPH_FOUND,
                            notify
                        ]
            
                        return result
                        
                    
                    col_sort = ['MAHDOUDE', 'AQUIFER', 'LOCATION', 'DATE_GREGORIAN']                    
                    df = df.sort_values(by=col_sort).reset_index(drop=True)
                                        
                    fig = go.Figure()
                    
                    fig.add_trace(
                        go.Scatter(
                            x=df['DATE_GREGORIAN'],
                            y=df['WATER_TABLE'],
                            mode='lines+markers',
                            name=f'داده‌های کنترل کیفی شده',
                            marker=dict(
                                color='blue',
                                size=10,
                            ),
                            line=dict(
                                color='black',
                                width=1
                            )  
                        )
                    )
                    
                    tmp = df[df["DESCRIPTION"].str.contains("روش بازسازی")]
                                        
                    fig.add_trace(
                        go.Scatter(
                            x=tmp['DATE_GREGORIAN'],
                            y=tmp['WATER_TABLE'],
                            mode='markers',
                            name=f'داده‌های بازسازی شده',
                            marker=dict(
                                color='red',
                                size=10,
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
                        color = 'green',
                        action = "hide",
                    )
                    
                    result = [
                        fig,
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
                NO_MATCHING_GRAPH_FOUND,
                notify
            ]
            
            return result


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
    # CALLBACK: SAVE SYNCDATE DATA
    # -----------------------------------------------------------------------------  
    @app.callback(
        Output('SAVE_SYNC_DATE_BUTTON', 'n_clicks'),
        Output("ALERTS", "children"),
        Input('SAVE_SYNC_DATE_BUTTON', 'n_clicks'),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        Input('SAVE_SYNC_DAY', 'value'),
        Input('SAVE_WHICH_WELL', 'value'),
    ) 
    def save_syncdate(
        n, study_area, aquifer, well, day, which_well
    ):
        if n != 0:
            
            if which_well is not None:
                
                table_exist = find_table(
                    database=POSTGRES_DB_DATA,
                    table=DB_DATA_TABLE_SYNCDATEDATA,
                    user=POSTGRES_USER_NAME,
                    password=POSTGRES_PASSWORD,
                    host=POSTGRES_HOST,
                    port=POSTGRES_PORT
                )
                
                if which_well == 0:

                    sql = f"SELECT * FROM {DB_DATA_TABLE_INTERPOLATEDDATA}"

                    df = pd.read_sql_query(
                        sql = sql,
                        con = ENGINE_DATA
                    )
                    
                    if len(df) == 0:
                
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خطا",
                            message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی انجام دهید."],
                            color = 'red',
                            action = "show",
                            autoClose=10000
                        )
                        
                        result = [
                            0,
                            notify
                        ]
                        
                        return result
                                            
                    df = df.groupby(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                    ).apply(lambda x: f_syncdate(
                        df=x,
                        day=day
                    )).reset_index(drop=True)
                    
                    df = df.sort_values(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                    )
                    
                    update_table(
                        data=df,
                        table_exist=table_exist,
                        table_name=DB_DATA_TABLE_SYNCDATEDATA,
                        engine=ENGINE_DATA,
                        study_area=None,
                        aquifer=None,
                        well=None,
                    )
                    
                    update_table_data(
                        table_name_syncdate=DB_DATA_TABLE_SYNCDATEDATA,
                        table_name_data=DB_DATA_TABLE_DATA,
                        engine=ENGINE_DATA,
                        database=POSTGRES_DB_DATA,
                        user=POSTGRES_USER_NAME,
                        password=POSTGRES_PASSWORD,
                        host=POSTGRES_HOST,
                        port=POSTGRES_PORT
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
                    
                    sql = f"SELECT * FROM {DB_DATA_TABLE_INTERPOLATEDDATA} WHERE \"MAHDOUDE\" = '{study_area}'"

                    df = pd.read_sql_query(
                        sql = sql,
                        con = ENGINE_DATA
                    )
                    
                    if len(df) == 0:
                
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خطا",
                            message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی انجام دهید."],
                            color = 'red',
                            action = "show",
                            autoClose=10000
                        )
                        
                        result = [
                            0,
                            notify
                        ]
                        
                        return result
                    
                    df = df.groupby(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                    ).apply(lambda x: f_syncdate(
                        df=x,
                        day=day
                    )).reset_index(drop=True)
                    
                    df = df.sort_values(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                    )
                                        
                    update_table(
                        data=df,
                        table_exist=table_exist,
                        table_name=DB_DATA_TABLE_SYNCDATEDATA,
                        engine=ENGINE_DATA,
                        study_area=study_area,
                        aquifer=None,
                        well=None,
                    )
                    
                    update_table_data(
                        table_name_syncdate=DB_DATA_TABLE_SYNCDATEDATA,
                        table_name_data=DB_DATA_TABLE_DATA,
                        engine=ENGINE_DATA,
                        database=POSTGRES_DB_DATA,
                        user=POSTGRES_USER_NAME,
                        password=POSTGRES_PASSWORD,
                        host=POSTGRES_HOST,
                        port=POSTGRES_PORT
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
                    
                    sql = f"SELECT * FROM {DB_DATA_TABLE_INTERPOLATEDDATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'"

                    df = pd.read_sql_query(
                        sql = sql,
                        con = ENGINE_DATA
                    )

                    if len(df) == 0:
                
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خطا",
                            message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی انجام دهید."],
                            color = 'red',
                            action = "show",
                            autoClose=10000
                        )
                        
                        result = [
                            0,
                            notify
                        ]
                        
                        return result
                    
                                            
                    df = df.groupby(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                    ).apply(lambda x: f_syncdate(
                        df=x,
                        day=day
                    )).reset_index(drop=True)
                    
                    df = df.sort_values(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                    )
                                            
                    update_table(
                        data=df,
                        table_exist=table_exist,
                        table_name=DB_DATA_TABLE_SYNCDATEDATA,
                        engine=ENGINE_DATA,
                        study_area=study_area,
                        aquifer=aquifer,
                        well=None,
                    )
                    
                    update_table_data(
                        table_name_syncdate=DB_DATA_TABLE_SYNCDATEDATA,
                        table_name_data=DB_DATA_TABLE_DATA,
                        engine=ENGINE_DATA,
                        database=POSTGRES_DB_DATA,
                        user=POSTGRES_USER_NAME,
                        password=POSTGRES_PASSWORD,
                        host=POSTGRES_HOST,
                        port=POSTGRES_PORT
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
                    
                    sql = f"SELECT * FROM {DB_DATA_TABLE_INTERPOLATEDDATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"

                    df = pd.read_sql_query(
                        sql = sql,
                        con = ENGINE_DATA
                    )
                    
                    if len(df) == 0:
                
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خطا",
                            message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی انجام دهید."],
                            color = 'red',
                            action = "show",
                            autoClose=10000
                        )
                        
                        result = [
                            0,
                            notify
                        ]
                        
                        return result
                                            
                    df = df.groupby(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                    ).apply(lambda x: f_syncdate(
                        df=x,
                        day=day
                    )).reset_index(drop=True)
                    
                    df = df.sort_values(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                    )
                                            
                    update_table(
                        data=df,
                        table_exist=table_exist,
                        table_name=DB_DATA_TABLE_SYNCDATEDATA,
                        engine=ENGINE_DATA,
                        study_area=study_area,
                        aquifer=aquifer,
                        well=well,
                    )
                    
                    update_table_data(
                        table_name_syncdate=DB_DATA_TABLE_SYNCDATEDATA,
                        table_name_data=DB_DATA_TABLE_DATA,
                        engine=ENGINE_DATA,
                        database=POSTGRES_DB_DATA,
                        user=POSTGRES_USER_NAME,
                        password=POSTGRES_PASSWORD,
                        host=POSTGRES_HOST,
                        port=POSTGRES_PORT
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
                    message = ["محدوده هماهنگ‌سازی تاریخ انتخاب نشده است!"],
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
        

    @app.callback(
        Output("DOWNLOAD_XLSX", "data"),
        Input("BTN_XLSX", "n_clicks"),
        prevent_initial_call=True
    )
    def generate_xlsx(
        n_nlicks,
    ):
        if n_nlicks != 0:
                        
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
                
            if DB_DATA_TABLE_SYNCDATEDATA in table_name_list_exist:
            
                df = pd.read_sql_query(
                    sql = f"SELECT * FROM {DB_DATA_TABLE_SYNCDATEDATA}",
                    con = ENGINE_DATA
                )
                
                geoinfo = pd.read_sql_query(
                    sql='SELECT * FROM geoinfo',
                    con=ENGINE_DATA
                )

                def to_xlsx(bytes_io):
                    xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
                    geoinfo.to_excel(xslx_writer, index=False, sheet_name="GeoInfo")
                    df.to_excel(xslx_writer, index=False, sheet_name="Data")
                    xslx_writer.save()

                return dcc.send_bytes(to_xlsx, "data.xlsx")
            
            else:
                
                return no_update
        
        return no_update