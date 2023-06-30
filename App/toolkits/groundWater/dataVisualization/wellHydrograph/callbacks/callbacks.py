import json
import itertools
from os import stat_result
import tempfile
import numpy as np
import pandas as pd
import geopandas as gpd
import psycopg2
import statistics
from geoalchemy2 import Geometry, WKTElement
from dash import no_update, dcc, dash_table, html
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
from . import *


def toolkits__groundWater__dataVisualization__wellHydrograph__callbacks(app):
    
    # -----------------------------------------------------------------------------
    # CALLBACK: SELECT STUDYAREA
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('STUDY_AREA_SELECT', 'options'),
        Output("ALERTS", "children"),
        Input('INTERVAL-STUDYAREA', 'n_intervals'),
    )
    def study_area_select(
        n
    ):
        
        table_data_exist = find_table(
            database=POSTGRES_DB_DATA,
            table=DB_DATA_TABLE_DATA,
            user=POSTGRES_USER_NAME,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )
        
        table_mahdoude_exist = find_table(
            database=POSTGRES_DB_LAYERS,
            table=DB_LAYERS_TABLE_MAHDOUDE,
            user=POSTGRES_USER_NAME,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )

        if table_data_exist and table_mahdoude_exist:
            
            mahdoude_data = pd.read_sql_query(
                sql=f'SELECT DISTINCT "MAHDOUDE" FROM {DB_DATA_TABLE_DATA};',
                con=ENGINE_DATA
            )
            
            mahdoude_data = mahdoude_data['MAHDOUDE'].values.tolist()
            
            mahdoude_layers = pd.read_sql_query(
                sql=f'SELECT DISTINCT "MAHDOUDE" FROM {DB_LAYERS_TABLE_MAHDOUDE};',
                con=ENGINE_LAYERS
            )
            
            mahdoude_layers = mahdoude_layers['MAHDOUDE'].values.tolist()
            
            if all([mah in mahdoude_layers for mah in mahdoude_data]):
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "",
                    message = [""],
                    color = 'red',
                    action = "hide"
                )
                
                result = [
                    [{'label': i, 'value': i} for i in sorted(mahdoude_data)],
                    notify
                ]
                
                return result
        
            else:
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["در فایل داده‌ها محدوده‌هایی وجود دارد که در لایه محدوده‌ها وجود ندارد."],
                    color = 'red',
                    action = "show"
                )
                
                result = [
                    [{}],
                    notify
                ]
                
                return result
        
        else:
            
            notify = dmc.Notification(
                id ="notify",
                title = "",
                message = [""],
                color = 'red',
                action = "hide"
            )
            
            result = [
                [{}],
                notify
            ]
            
            return result
    
    
    # -----------------------------------------------------------------------------
    # CALLBACK: SELECT AQUIFER
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('AQUIFER_SELECT', 'options'),
        Output("ALERTS", "children"),
        Input('STUDY_AREA_SELECT', 'value'),
    )
    def aquifer_select(
        study_area_selected
    ):
        if study_area_selected is not None and len(study_area_selected) != 0:
            
            REDIS_DB.set('wellHydrograph_studyArea', study_area_selected)
            
            df_aquifer_data = pd.read_sql_query(
                sql=f"SELECT DISTINCT \"MAHDOUDE\", \"AQUIFER\" FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\"='{study_area_selected}';",
                con=ENGINE_DATA
            )
                    
            aquifer_data = df_aquifer_data['AQUIFER'].values.tolist()
            
            df_aquifer_layers = pd.read_sql_query(
                sql=f"SELECT DISTINCT \"MAHDOUDE\", \"AQUIFER\" FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\"='{study_area_selected}';",
                con=ENGINE_LAYERS
            )
                        
            aquifer_layers = df_aquifer_layers['AQUIFER'].values.tolist()
            
            if all(row in aquifer_layers for row in aquifer_data):
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "",
                    message = [""],
                    color = 'red',
                    action = "hide"
                )
                
                result = [
                    [{'label': i, 'value': i} for i in sorted(aquifer_data)],
                    notify
                ]
                
                return result
            
            else:
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["در فایل داده‌ها آبخوان‌هایی وجود دارد که در لایه آبخوان‌ها وجود ندارد."],
                    color = 'red',
                    action = "show"
                )
                
                result = [
                    [{}],
                    notify
                ]
                
                return result
            
        else:
            
            notify = dmc.Notification(
                id ="notify",
                title = "",
                message = [""],
                color = 'red',
                action = "hide"
            )
            
            result = [
                [{}],
                notify
            ]
            
            return result
    
    # -----------------------------------------------------------------------------
    # CALLBACK: SELECT WELL
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('WELL_SELECT', 'options'),
        Output("ALERTS", "children"),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
    )
    def well_select(
        study_area_selected,
        aquifer_selected,
    ):
        if (study_area_selected is not None) and (len(study_area_selected) != 0) and\
            (aquifer_selected is not None) and (len(aquifer_selected) != 0):
                
                REDIS_DB.set('wellHydrograph_aquifer', aquifer_selected)

                df_well_data = pd.read_sql_query(
                    sql=f"SELECT DISTINCT \"MAHDOUDE\", \"AQUIFER\", \"LOCATION\" FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\"='{study_area_selected}' AND \"AQUIFER\"='{aquifer_selected}';",
                    con=ENGINE_DATA
                )
                        
                well_data = df_well_data['LOCATION'].values.tolist()
                
                df_well_layers = pd.read_sql_query(
                    sql=f"SELECT DISTINCT \"MAHDOUDE\", \"AQUIFER\", \"LOCATION\" FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\"='{study_area_selected}' AND \"AQUIFER\"='{aquifer_selected}';",
                    con=ENGINE_LAYERS
                )
                            
                well_layers = df_well_layers['LOCATION'].values.tolist()
                
                if all(row in well_layers for row in well_data):
                    
                    notify = dmc.Notification(
                        id ="notify",
                        title = "",
                        message = [""],
                        color = 'red',
                        action = "hide"
                    )
                    
                    result = [
                        [{'label': i, 'value': i} for i in sorted(well_data)],
                        notify
                    ]
                    
                    return result
                
                else:
                    
                    notify = dmc.Notification(
                        id ="notify",
                        title = "خطا",
                        message = ["در فایل داده‌ها چاه‌هایی وجود دارد که در لایه چاه‌ها وجود ندارد."],
                        color = 'red',
                        action = "show"
                    )
                    
                    result = [
                        [{}],
                        notify
                    ]
                    
                    return result
                
        else:
            
            notify = dmc.Notification(
                id ="notify",
                title = "",
                message = [""],
                color = 'red',
                action = "hide"
            )
            
            result = [
                [{}],
                notify
            ]
            
            return result

    
    
    # # -----------------------------------------------------------------------------
    # # CALLBACK: UPDATE DROPDOWN LIST
    # # -----------------------------------------------------------------------------
    # @app.callback(
    #     Output('STUDY_AREA_SELECT', 'value'),
    #     Output('AQUIFER_SELECT', 'value'),
    #     Output('WELL_SELECT', 'value'),
    #     Output('START_MONTH', 'value'),
    #     Output("START_YEAR", "value"),
    #     Output('END_MONTH', 'value'),
    #     Output("END_YEAR", "value"),
    #     Input('STUDY_AREA_SELECT', 'value'),
    #     Input('AQUIFER_SELECT', 'value'),
    #     Input('WELL_SELECT', 'value'),
    #     Input('START_MONTH', 'value'),
    #     Input("START_YEAR", "value"),
    #     Input('END_MONTH', 'value'),
    #     Input("END_YEAR", "value"),
    # )
    # def update_dropdown_list(
    #     study_area, aquifer, well, s_m, s_y, e_m, e_y
    # ):
    #     if (study_area is not None and len(study_area) != 0) and\
    #         (aquifer is None or len(aquifer) == 0) and\
    #             (well is not None and len(well) != 0):
                                
    #         result = [
    #             no_update,
    #             [],
    #             [],
    #             None,
    #             None,
    #             None,
    #             None,
    #         ]
            
    #         return result
        
    #     elif (study_area is None or len(study_area) == 0) and\
    #         (aquifer is not None and len(aquifer) != 0) and\
    #             (well is not None and len(well) != 0):
                        
    #         result = [
    #             [],
    #             [],
    #             [],
    #             None,
    #             None,
    #             None,
    #             None,
    #         ]
            
    #         return result
        
    #     elif (study_area != REDIS_DB.get('wellHydrograph_studyArea').decode('utf-8')):
            
    #         result = [
    #             no_update,
    #             [],
    #             [],
    #             None,
    #             None,
    #             None,
    #             None,
    #         ]
            
    #         return result
        
    #     elif (aquifer != REDIS_DB.get('wellHydrograph_aquifer').decode('utf-8')):
            
    #         result = [
    #             no_update,
    #             no_update,
    #             [],
    #             None,
    #             None,
    #             None,
    #             None,
    #         ]
            
    #         return result
            
        
    #     else:
                        
    #         result = [
    #             no_update,
    #             no_update,
    #             no_update,
    #             no_update,
    #             no_update,
    #             no_update,
    #             no_update,
    #         ]
            
    #         return result


    # -----------------------------------------------------------------------------
    # CALLBACK: MAP
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
                (well is not None and len(well) != 0):
                    
                    #* MAHDOUDE:
                    
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_MAHDOUDE} WHERE \"MAHDOUDE\" = '{study_area}'"
                    
                    df_study_area = gpd.GeoDataFrame.from_postgis(
                        sql=sql,
                        con=ENGINE_LAYERS,
                        geom_col="geometry"
                    )
                    
                    df_study_area_json = json.loads(df_study_area.to_json())
                    
                    for feature in df_study_area_json["features"]:
                        feature['id'] = feature['properties']['MAHDOUDE']
                    
                    #* AQUIFER:
                    
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'"
                    
                    df_aquifer = gpd.GeoDataFrame.from_postgis(
                        sql=sql,
                        con=ENGINE_LAYERS,
                        geom_col="geometry"
                    )
                    
                    df_aquifer_json = json.loads(df_aquifer.to_json())
                    
                    for feature in df_aquifer_json["features"]:
                        feature['id'] = feature['properties']['AQUIFER']
                    
                    #* SELECTED WELL:
                    
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"
                    
                    df_well = gpd.GeoDataFrame.from_postgis(
                        sql=sql,
                        con=ENGINE_LAYERS,
                        geom_col="geometry"
                    )
                    
                    #* ALL WELL:
                    
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

        else:
            
            return BASE_MAP
    
    # -----------------------------------------------------------------------------
    # CALLBACK: SELECT DATE
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('START_MONTH', 'options'),
        Output("START_YEAR", "options"),
        Output('END_MONTH', 'options'),
        Output("END_YEAR", "options"),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        State('AQUIFER_SELECT', 'value'),
    )
    def select_date(
        study_area, aquifer, well, aquifer_state
    ):
        if (study_area is not None and len(study_area) != 0) and (aquifer is not None and len(aquifer) != 0) and (well is not None and len(well) != 0):
                                  
            sql = f"SELECT * FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}';"
            
            data = pd.read_sql_query(
                sql=sql,
                con=ENGINE_DATA
            ).sort_values(
                ["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
            ).reset_index(drop=True)
                        
            result = [
                [{'label': i, 'value': i} for i in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]],
                [{'label': str(i), 'value': str(i)} for i in list(range(int(min(data["YEAR_PERSIAN"])), int(max(data["YEAR_PERSIAN"])) + 1))],
                [{'label': i, 'value': i} for i in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]],
                [{'label': str(i), 'value': str(i)} for i in list(range(int(min(data["YEAR_PERSIAN"])), int(max(data["YEAR_PERSIAN"])) + 1))]
            ]
            
            return result
            
        else:
            
            result = [
                [{}],
                [{}],
                [{}],
                [{}]
            ]
            
            return result
    
    # -----------------------------------------------------------------------------
    # CALLBACK: GRAPH & TABLE
    # -----------------------------------------------------------------------------  
    @app.callback(
        Output('HYDROGRAPH_GRAPH', 'children'),
        Output('HYDROGRAPH_TABLE', 'children'),
        Output("DIV_DOWNLOAD_DATA", "hidden"),
        Output("STORAGE-WELL-HYDROGRAPH", "data"),       
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        Input('START_MONTH', 'value'),
        Input("START_YEAR", "value"),
        Input('END_MONTH', 'value'),
        Input("END_YEAR", "value"),
    ) 
    def graph_table(
        study_area, aquifer, well, s_m, s_y, e_m, e_y
    ):
        if (study_area is not None and len(study_area) != 0) and (aquifer is not None and len(aquifer) != 0) and (well is not None and len(well) != 0):
            
            sql = f"SELECT * FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}';"
            
            data = pd.read_sql_query(
                sql=sql,
                con=ENGINE_DATA
            ).sort_values(
                ["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
            ).reset_index(drop=True)
            
            if (s_m is not None) and (s_y is not None) and (e_m is not None) and (e_y is not None):
                
                start_date = f"{s_y}-{s_m}"
                end_date = f"{e_y}-{e_m}"
                
                data["YM_PERSIAN"] = data["YEAR_PERSIAN"] + "-" + data["MONTH_PERSIAN"]                
                data = data.loc[((data["YM_PERSIAN"] >= start_date) & (data["YM_PERSIAN"] <= end_date)), :]
                
                data = data.sort_values(
                    ["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                ).reset_index(drop=True)
            
            if data.shape[0] >= 1:
            
            
                data_table = data[["YEAR_PERSIAN", "MONTH_PERSIAN", "WATER_LEVEL"]]
                data_table["YEAR_PERSIAN"] = data_table["YEAR_PERSIAN"].astype(int)
                data_table["MONTH_PERSIAN"] = data_table["MONTH_PERSIAN"].astype(int)
                data_table.columns = ["سال", "ماه", "پارامتر"]
                data_table = resultTable(data_table)
                data_table.columns = [
                    "سال",
                    "ماه",
                    "تراز ماهانه سطح آب",
                    "سال آبی",
                    "ماه آبی",
                    "تغییرات تراز سطح آب نسبت به ماه قبل",
                    "تغییرات تراز سطح آب نسبت به ماه سال قبل"
                ]
                
                sm_start = pd.DataFrame(
                    
                    {
                        "سال آبی": [data_table["سال آبی"].to_list()[0]] * 12,
                        "ماه آبی": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    }
                    
                )
                
                data_table = data_table.merge(
                    sm_start,
                    how="outer",
                    on=["سال آبی", "ماه آبی"]
                )

                data_table.drop_duplicates(subset=["سال آبی", "ماه آبی"], keep="first", inplace=True)
                
                data_table = data_table.sort_values(
                ["سال آبی", "ماه آبی"]
                ).reset_index(drop=True)
                
                if len(data_table["سال آبی"].to_list()) > 1:
                
                    sm_end = pd.DataFrame(
                        
                        {
                            "سال آبی": [data_table["سال آبی"].to_list()[-1]] * 12,
                            "ماه آبی": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        }
                        
                    )
                    
                    data_table = data_table.merge(
                        sm_end,
                        how="outer",
                        on=["سال آبی", "ماه آبی"]
                    )
                    
                    data_table.drop_duplicates(subset=["سال آبی", "ماه آبی"], keep="first", inplace=True)
                            
                    data_table = data_table.sort_values(
                    ["سال آبی", "ماه آبی"]
                    ).reset_index(drop=True)
                
                download_data = data_table.copy()                
                download_data = download_data.dropna(subset=["سال", "ماه"])
                
                data_table = data_table.pivot_table(
                    values="تغییرات تراز سطح آب نسبت به ماه قبل",
                    index="سال آبی",
                    columns="ماه آبی",
                    dropna=False
                ).reset_index()
                
                data_table.columns = ["سال آبی", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند", "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور"]
                
                data_table["مجموع سالانه"] = data_table.iloc[:,1:13].sum(axis=1).round(2)
                data_table["تجمعی مجموع سالانه"] = data_table["مجموع سالانه"].cumsum(skipna=True).round(2)            
                
                fig = go.Figure()
                            
                fig.add_trace(
                    go.Scatter(
                        x=data["DATE_GREGORIAN"],
                        y=data["WATER_LEVEL"],
                        name="داده‌های کنترل کیفی شده",
                        mode="lines+markers",
                        marker=dict(
                            color="blue",
                            size=10,
                        ),
                        line=dict(
                            color="blue",
                            width=1
                        ),
                        line_shape='spline'
                    )
                )
                
                tmp = data[data["DESCRIPTION"].str.contains("روش بازسازی")]
                
                fig.add_trace(
                    go.Scatter(
                        x=tmp["DATE_GREGORIAN"],
                        y=tmp["WATER_LEVEL"],
                        name="داده‌های بازسازی شده",
                        mode="markers",
                        marker=dict(
                            color="red",
                            size=10,
                        ),
                    )
                )
                
                tmp = data[data["DESCRIPTION"].str.contains("اصلاح")]

                fig.add_trace(
                    go.Scatter(
                        x=tmp['DATE_GREGORIAN'],
                        y=tmp['WATER_LEVEL'],
                        name=f'داده‌های اصلاح شده',
                        mode='markers',
                        marker=dict(
                            color='green',
                            size=10,
                        ),
                    )
                )

                fig.update_layout(
                    hoverlabel=dict(
                        namelength = -1
                    ),
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
                    yaxis=dict(
                        tickformat=".1f",
                    ),
                    title=dict(
                        text=f"تراز ماهانه سطح آب چاه «{well}» بر حسب متر",
                        yanchor="top",
                        y=0.99,
                        xanchor="center",
                        x=0.500
                    ),
                    margin=dict(
                        l=50,
                        r=30,
                        b=30,
                        t=30,
                        pad=0
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=0.01,
                        xanchor="center",
                        x=0.5
                    )
                )
                
                fig.update_xaxes(
                    calendar='jalali',
                    tickformat="%Y-%m-%d",
                )
                
                table_content = dash_table.DataTable(
                    columns=[
                        {"name": i, "id": i} for i in data_table.columns
                    ],
                    data=data_table.to_dict('records'),
                    page_size=10,
                    style_as_list_view=True,
                    style_table={
                        # 'overflowX': 'auto',
                        'overflowY': 'auto',
                        'direction': 'rtl',
                    },
                    style_cell={
                        'font-family': "Vazir-Regular-FD",
                        'border': '1px solid grey',
                        'font-size': '14px',
                        'text_align': 'center',
                        'minWidth': 50,
                        'maxWidth': 100,
                        'direction': 'ltr',
                        'padding': '5px',
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
                
                result = [
                    dcc.Graph(
                        figure=fig
                    ),
                    [
                        html.H5(children=f'تغییرات تراز سطح آب زیرزمینی نسبت به ماه قبل (متر) - {well}'),
                        table_content
                    ],
                    False,
                    download_data.to_dict('records')
                    
                ]
                
                return result
            
            else:
                
                result = [
                    dcc.Graph(
                        figure=NO_MATCHING_GRAPH_FOUND
                    ),
                    dcc.Graph(
                        figure=NO_MATCHING_TABLE_FOUND
                    ),
                    True,
                    {}
                ]
                
                return result
        
        else:
            
            result = [
                dcc.Graph(
                    figure=NO_MATCHING_GRAPH_FOUND
                ),
                dcc.Graph(
                    figure=NO_MATCHING_TABLE_FOUND
                ),
                True,
                {}
            ]
            
            return result
    
    
    @app.callback(
        Output("DOWNLOAD_XLSX", "data"),
        Input("BTN_XLSX", "n_clicks"),
        State("STORAGE-WELL-HYDROGRAPH", "data"),
        prevent_initial_call=True
    )
    def generate_xlsx(
        n_nlicks, data
    ):
        if n_nlicks != 0:
            
            df = pd.DataFrame(data)

            def to_xlsx(bytes_io):
                xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")
                df.to_excel(xslx_writer, index=False, sheet_name="sheet1")
                xslx_writer.save()

            return dcc.send_bytes(to_xlsx, "data.xlsx")