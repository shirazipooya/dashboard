import json
import itertools
from os import stat_result
import tempfile
import numpy as np
import pandas as pd
import geopandas as gpd
import psycopg2
import swifter
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
            
            if all(row in df_aquifer_layers for row in df_aquifer_data):
                
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
                
                if all(row in df_well_layers for row in df_well_data):
                    
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

    
    
    # -----------------------------------------------------------------------------
    # CALLBACK: UPDATE DROPDOWN LIST
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('STUDY_AREA_SELECT', 'value'),
        Output('AQUIFER_SELECT', 'value'),
        Output('WELL_SELECT', 'value'),
        Output('START_MONTH', 'value'),
        Output("START_YEAR", "value"),
        Output('END_MONTH', 'value'),
        Output("END_YEAR", "value"),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        Input('START_MONTH', 'value'),
        Input("START_YEAR", "value"),
        Input('END_MONTH', 'value'),
        Input("END_YEAR", "value"),
    )
    def update_dropdown_list(
        study_area, aquifer, well, s_m, s_y, e_m, e_y
    ):
        if (study_area is not None and len(study_area) != 0) and\
            (aquifer is None or len(aquifer) == 0) and\
                (well is not None and len(well) != 0):
            
            result = [
                no_update,
                [],
                [],
                None,
                None,
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
                None,
                None,
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
                no_update,
            ]
            
            return result


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
    )
    def select_date(
        study_area, aquifer, well,
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
            
    
    
    # # -----------------------------------------------------------------------------
    # # CALLBACK: CALCULATE UNIT HYDROGRAPH
    # # -----------------------------------------------------------------------------
    # @app.callback(
    #     Output('CALCULATE_UNIT_HYDROGRAPH', 'n_clicks'),
    #     Output("ALERTS", "children"),
    #     Output('INTERVAL', 'n_intervals'),
    #     Input('CALCULATE_UNIT_HYDROGRAPH', 'n_clicks'),
    #     State('STUDY_AREA_SELECT', 'value'),
    #     State('AQUIFER_SELECT', 'value'),
    #     State('WELL_SELECT', 'value'),
    #     State('STORAGE_COEFFICIENT', 'value'),
    #     State('UNIT_HYDROGRAPH_METHOD', 'value'),
    # )
    # def calculate_unit_hydrograph(
    #     n, study_area, aquifer, well, sc, methods
    # ):
    #     if n != 0:
            
    #         if (study_area is not None and len(study_area) != 0) and (aquifer is not None and len(aquifer) != 0) and (well is not None and len(well) != 0):
                
    #             if sc is not None:
                    
    #                 if methods is not None and len(methods) != 0:
                        
    #                     #* GEODATAFRAME AQUIFER:
    #                     sql = f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}';"
                        
    #                     gdf_db_layers_table_aquifer = gpd.GeoDataFrame.from_postgis(
    #                         sql=sql,
    #                         con=ENGINE_LAYERS,
    #                         geom_col="geometry"
    #                     )
                        
    #                     #* GEODATAFRAME SELECTED WELL:
    #                     sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" IN {*well,};"
                        
    #                     gdf_db_layers_table_well = gpd.GeoDataFrame.from_postgis(
    #                         sql=sql,
    #                         con=ENGINE_LAYERS,
    #                         geom_col="geometry"
    #                     )
                        
    #                     #* DATAFRAME WATER LEVEL DATA:
    #                     sql = f"SELECT * FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" IN {*well,};"
                        
    #                     df_db_data_table_data = pd.read_sql_query(
    #                         sql=sql,
    #                         con=ENGINE_DATA
    #                     ).sort_values(
    #                         ["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
    #                     ).reset_index(drop=True)
                        
    #                     #* ADD STORAGE COEFFICIENTS TO DATAFRAME WATER LEVEL:
    #                     df_db_data_table_data["STORAGE_COEFFICIENT"] = sc
                        
    #                     # WARNING: FOR DIFFERENT DAY OF MONTH, THIS METHOD MUST BE MODIFY.
                        
    #                     result = pd.DataFrame(
    #                         columns=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                     )
                        
    #                     for m in methods:
                            
    #                         if m in ["AM", "GM", "HM", "ME"]:
                                
    #                             st = {
    #                                 "AM": statistics.mean,
    #                                 "GM": statistics.geometric_mean,
    #                                 "HM": statistics.harmonic_mean,
    #                                 "ME": statistics.median,
    #                             }
                                
    #                             tmp = df_db_data_table_data[
    #                                 ["MAHDOUDE", "AQUIFER", "LOCATION", "YEAR_PERSIAN", "MONTH_PERSIAN", "WATER_LEVEL"]
    #                             ]
                                                                
    #                             tmp = tmp.groupby(
    #                                 by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).agg({
    #                                 "WATER_LEVEL": st[m]
    #                             }).reset_index()
                                
    #                             tmp = tmp.sort_values(
    #                                 by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).reset_index(drop=True).rename(columns={"WATER_LEVEL" : f"UNIT_HYDROGRAPH_{m}"})
                                
                                
    #                             result = result.merge(
    #                                 tmp, 
    #                                 how="outer", 
    #                                 on=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).sort_values(
    #                                 by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).reset_index(drop=True)
                                
    #                         if m == "TWA":
                                
    #                             tmp_data = df_db_data_table_data[
    #                                 ["MAHDOUDE", "AQUIFER", "LOCATION", "YEAR_PERSIAN", "MONTH_PERSIAN", "WATER_LEVEL", "STORAGE_COEFFICIENT"]
    #                             ]
                                
    #                             tmp_thissen = tmp_data.swifter.groupby(
    #                                 by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                                 ).apply(
    #                                     lambda x: calculate_thiessen_polygons(
    #                                         data=x,
    #                                         para="WATER_LEVEL",
    #                                         point=gdf_db_layers_table_well,
    #                                         point_name="LOCATION",
    #                                         limit=gdf_db_layers_table_aquifer
    #                                     )
    #                                 ).reset_index()
                                
    #                             tmp_thissen = tmp_thissen[['MAHDOUDE', 'AQUIFER', 'LOCATION', 'YEAR_PERSIAN', 'MONTH_PERSIAN', 'THISSEN_POINT', 'THISSEN_LIMIT', 'geometry']]
                                
    #                             tmp_thissen = tmp_thissen.rename(
    #                                 columns={
    #                                     "THISSEN_POINT" : "THISSEN_LOCATION",
    #                                     "THISSEN_LIMIT" : "THISSEN_AQUIFER",
    #                                 }
    #                             )
                                
    #                             tmp_thissen.to_postgis(
    #                                 name=DB_LAYERS_TABLE_TEMPORARY,
    #                                 con=ENGINE_LAYERS,
    #                                 if_exists='replace',
    #                                 index=False,
    #                                 dtype={'geometry': Geometry(srid= 4326)}
    #                             )
                                
    #                             tmp = tmp_data.merge(
    #                                 tmp_thissen, 
    #                                 how="left", 
    #                                 on=["MAHDOUDE", "AQUIFER", "LOCATION", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).sort_values(
    #                                 ["MAHDOUDE", "AQUIFER", "LOCATION", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).reset_index(drop=True)
                                
    #                             tmp['UNIT_HYDROGRAPH_TWA'] = (tmp["WATER_LEVEL"] * tmp['THISSEN_LOCATION']) / tmp['THISSEN_AQUIFER']
                                
    #                             tmp['STORAGE_COEFFICIENT_AQUIFER'] = (tmp["STORAGE_COEFFICIENT"] * tmp['THISSEN_LOCATION']) / tmp['THISSEN_AQUIFER']
                                
    #                             tmp = tmp.groupby(
    #                                 by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).agg({
    #                                 "UNIT_HYDROGRAPH_TWA": 'sum',
    #                                 "STORAGE_COEFFICIENT_AQUIFER": 'sum',
    #                                 "THISSEN_AQUIFER": 'mean', 
    #                             }).reset_index()
                                
    #                             tmp = tmp.sort_values(
    #                                 by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).reset_index(drop=True)
                                
    #                             result = result.merge(
    #                                 tmp[['MAHDOUDE', 'AQUIFER', 'YEAR_PERSIAN', 'MONTH_PERSIAN', 'UNIT_HYDROGRAPH_TWA']], 
    #                                 how="outer", 
    #                                 on=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).sort_values(
    #                                 by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).reset_index(drop=True)
                                
    #                             #* TWA ADJUSTED
                                
    #                             median_diff = tmp_data.groupby(by=["MAHDOUDE", "AQUIFER", "LOCATION"])["WATER_LEVEL"].diff().reset_index(drop=True).abs().median()

    #                             df_thiessen_change = tmp_data.swifter.groupby(by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"])["LOCATION"]\
    #                                 .apply(list)\
    #                                     .reset_index(name='LOCATION_LIST').sort_values(["YEAR_PERSIAN", "MONTH_PERSIAN"])
                                                        
    #                             df_thiessen_change_aquifer = df_thiessen_change.groupby(by=["MAHDOUDE", "AQUIFER"])\
    #                                 .apply(check_thiessen_change).reset_index(drop=True)
                                
    #                             result = result.merge(
    #                                 right=df_thiessen_change_aquifer[["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN", "THISSEN_CHANGE"]],
    #                                 how='left',
    #                                 on=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             ).sort_values(["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"])
                                                
    #                             tmp = result.copy()
    #                             tmp['DELTA'] = tmp['UNIT_HYDROGRAPH_TWA'].diff().fillna(0)
    #                             tmp['UNIT_HYDROGRAPH_TWA_ADJ'] = tmp['UNIT_HYDROGRAPH_TWA']
    #                             tmp["YM_PERSIAN"] = tmp["YEAR_PERSIAN"] + "-" + tmp["MONTH_PERSIAN"]
    #                             n = tmp[tmp["THISSEN_CHANGE"]]["YM_PERSIAN"].tolist()
                                
    #                             if len(n) > 0:                    
    #                                 for dt in n:                
    #                                     delta = tmp.loc[tmp["YM_PERSIAN"] == dt, "DELTA"].reset_index()["DELTA"][0]
    #                                     if delta >= 0:
    #                                         if abs(delta) > abs(median_diff):
    #                                             delta = delta - median_diff
    #                                         else:
    #                                             delta = 0
    #                                     else:
    #                                         if abs(delta) > abs(median_diff):
    #                                             delta = delta + median_diff
    #                                         else:
    #                                             delta = 0
                                            
    #                                     ix = tmp.loc[tmp["YM_PERSIAN"] == dt, "DELTA"].reset_index()["index"][0]
    #                                     tmp['TMP'] = tmp['UNIT_HYDROGRAPH_TWA_ADJ']
                                        
    #                                     for i in range(ix):                    
    #                                         tmp['TMP'][i] = tmp['UNIT_HYDROGRAPH_TWA_ADJ'][i] + delta                    
    #                                     tmp['UNIT_HYDROGRAPH_TWA_ADJ'] = tmp['TMP']
                                
    #                             result = result.merge(
    #                                 right=tmp[["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN", "UNIT_HYDROGRAPH_TWA_ADJ"]],
    #                                 how='left',
    #                                 on=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
    #                             )

    #                     result["YM_PERSIAN"] = result["YEAR_PERSIAN"] + "-" + result["MONTH_PERSIAN"]
    #                     result["DAY_PERSIAN"] = "01"                        
    #                     cols_p = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
    #                     cols_g = ['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']                       
    #                     result[cols_p] = result[cols_p].apply(pd.to_numeric, errors='coerce')
    #                     result[cols_p] = result[cols_p].astype(pd.Int64Dtype())
    #                     date_persian, date_gregorian = np.vectorize(check_persian_date_ymd)(result.YEAR_PERSIAN, result.MONTH_PERSIAN, result.DAY_PERSIAN)
    #                     result["DATE_PERSIAN"] = list(date_persian)
    #                     result["DATE_GREGORIAN"] = list(date_gregorian)
    #                     result[cols_p] = result['DATE_PERSIAN'].str.split('-', 2, expand=True)
    #                     result[cols_g] = result['DATE_GREGORIAN'].astype(str).str.split('-', 2, expand=True)
    #                     result["YEAR_PERSIAN"] = result["YEAR_PERSIAN"].astype(str).str.zfill(4)
    #                     result["MONTH_PERSIAN"] = result["MONTH_PERSIAN"].astype(str).str.zfill(2)
    #                     result["DAY_PERSIAN"] = result["DAY_PERSIAN"].astype(str).str.zfill(2)
    #                     result["YEAR_GREGORIAN"] = result["YEAR_GREGORIAN"].str.zfill(4)
    #                     result["MONTH_GREGORIAN"] = result["MONTH_GREGORIAN"].str.zfill(2)
    #                     result["DAY_GREGORIAN"] = result["DAY_GREGORIAN"].str.zfill(2)
    #                     result['DATE_PERSIAN'] = result["YEAR_PERSIAN"] + "-" + result["MONTH_PERSIAN"] + "-" + result["DAY_PERSIAN"]
    #                     result['DATE_GREGORIAN'] = result["YEAR_GREGORIAN"] + "-" + result["MONTH_GREGORIAN"] + "-" + result["DAY_GREGORIAN"]
    #                     result["DATE_GREGORIAN"] = result["DATE_GREGORIAN"].apply(pd.to_datetime)
                        
    #                     result.to_sql(
    #                         name=DB_DATA_TABLE_TEMPORARY,
    #                         con=ENGINE_DATA,
    #                         if_exists='replace',
    #                         index=False
    #                     )

    #                     notify = dmc.Notification(
    #                         id ="notify",
    #                         title = "خبر",
    #                         message = ["محاسبات با موفقیت انجام شد!"],
    #                         color = 'green',
    #                         action = "show"
    #                     )
                        
    #                     result = [
    #                         0,
    #                         notify,
    #                         0
    #                     ]
                        
    #                     return result
                    
    #                 else:
                        
    #                     notify = dmc.Notification(
    #                         id ="notify",
    #                         title = "خطا",
    #                         message = ["حداقل یک روش برای محاسبه هیدروگراف واحد آبخوان باید انتخاب گردد!"],
    #                         color = 'red',
    #                         action = "show"
    #                     )
                    
    #                     result = [
    #                         0,
    #                         notify,
    #                         1
    #                     ]
                    
    #                     return result
                
    #             else:
            
    #                 notify = dmc.Notification(
    #                     id ="notify",
    #                     title = "خطا",
    #                     message = ["ضریب ذخیره آبخوان وارد نشده است!"],
    #                     color = 'red',
    #                     action = "show"
    #                 )
                
    #                 result = [
    #                     0,
    #                     notify,
    #                     1
    #                 ]
                
    #                 return result
            
    #         else:
                
    #             notify = dmc.Notification(
    #                 id ="notify",
    #                 title = "خطا",
    #                 message = ["محدوده مطالعاتی یا آبخوان یا چاه‌های مشاهده‌ای انتخاب نشده‌اند!"],
    #                 color = 'red',
    #                 action = "show"
    #             )
            
    #             result = [
    #                 0,
    #                 notify,
    #                 1
    #             ]
            
    #             return result
                
        
    #     else:
            
    #         notify = dmc.Notification(
    #             id ="notify",
    #             title = "",
    #             message = [""],
    #             color = 'red',
    #             action = "hide"
    #         )
            
    #         result = [
    #             0,
    #             notify,
    #             1
    #         ]
            
    #         return result
    
    # -----------------------------------------------------------------------------
    # CALLBACK: GRAPH
    # -----------------------------------------------------------------------------  
    @app.callback(
        Output('HYDROGRAPH_GRAPH', 'children'),
        Output('HYDROGRAPH_TABLE', 'children'),        
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
                    ]
                    
                ]
                
                return result
            
            else:
                
                result = [
                    dcc.Graph(
                        figure=NO_MATCHING_GRAPH_FOUND
                    ),
                    dcc.Graph(
                        figure=NO_MATCHING_TABLE_FOUND
                    )
                ]
                
                return result
        
        else:
            
            result = [
                dcc.Graph(
                    figure=NO_MATCHING_GRAPH_FOUND
                ),
                dcc.Graph(
                    figure=NO_MATCHING_TABLE_FOUND
                )
            ]
            
            return result
            

    
    # # # -----------------------------------------------------------------------------
    # # # CALLBACK: SYNC DATE
    # # # -----------------------------------------------------------------------------  
    # # @app.callback(
    # #     Output('SYNC_DATE_BUTTON', 'n_clicks'),
    # #     Output('GRAPH_SYNCHRONIZED', 'figure'),
    # #     Output('DIV_GRAPH_SYNCHRONIZED', 'hidden'),
    # #     Output('DIV_GRAPH', 'hidden'),
    # #     Output("ALERTS", "children"),
        
    # #     Input('SYNC_DATE_BUTTON', 'n_clicks'),
    # #     Input('STUDY_AREA_SELECT', 'value'),
    # #     Input('AQUIFER_SELECT', 'value'),
    # #     Input('WELL_SELECT', 'value'),
    # #     Input('SYNC_DAY', 'value'),
    # # ) 
    # # def sync_date(
    # #     n, study_area, aquifer, well, day,
    # # ):
    # #     if n != 0:
            
    # #         if well is not None and len(well) != 0:
                
    # #             sql = f"SELECT * FROM {TABLE_NAME_INTERPOLATED_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"

    # #             df = pd.read_sql_query(
    # #                 sql = sql,
    # #                 con = ENGINE_DATA
    # #             )
                
    # #             if len(df) == 0:
                
    # #                 notify = dmc.Notification(
    # #                     id ="notify",
    # #                     title = "خطا",
    # #                     message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای یا محدوده مطالعاتی انجام دهید."],
    # #                     color = 'red',
    # #                     action = "show",
    # #                     autoClose=10000
    # #                 )
                    
    # #                 result = [
    # #                     0,
    # #                     NO_MATCHING_GRAPH_FOUND,
    # #                     True,
    # #                     False,
    # #                     notify
    # #                 ]
                    
    # #                 return result

    # #             tmp = df.groupby(
    # #                 by=["MAHDOUDE", "AQUIFER", "LOCATION"]
    # #             ).apply(lambda x: f_syncdate(
    # #                 df=x,
    # #                 day=day
    # #             )).reset_index(drop=True)
                            
    # #             tmp.sort_values(
    # #                 by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
    # #             ).reset_index(drop=True)
                
    # #             fig = go.Figure()
        
    # #             fig.add_trace(
    # #                 go.Scatter(
    # #                     x=df['DATE_GREGORIAN'],
    # #                     y=df['WATER_TABLE'],
    # #                     mode='lines+markers',
    # #                     name=f'داده‌های کنترل کیفی شده',
    # #                     marker=dict(
    # #                         color='blue',
    # #                         size=10,
    # #                     ),
    # #                     line=dict(
    # #                         color='black',
    # #                         width=0.5
    # #                     )  
    # #                 )
    # #             )
                
    # #             fig.add_trace(
    # #                 go.Scatter(
    # #                     x=tmp['DATE_GREGORIAN'],
    # #                     y=tmp['WATER_TABLE'],
    # #                     mode='lines+markers',
    # #                     name=f'داده‌های هماهنگ‌سازی شده تاریخ برای روز {day}ام',
    # #                     marker=dict(
    # #                         color='black',
    # #                         size=10,
    # #                     ),
    # #                     line=dict(
    # #                         color='black',
    # #                         width=1
    # #                     )  
    # #                 )
    # #             )
                
    # #             fig.update_layout(
    # #                 hoverlabel=dict(
    # #                     namelength = -1
    # #                 ),
    # #                 yaxis_title="عمق سطح آب - متر",
    # #                 xaxis_title='تاریخ',
    # #                 autosize=False,
    # #                 font=dict(
    # #                     family="Vazir-Regular-FD",
    # #                     size=14,
    # #                     color="RebeccaPurple"
    # #                 ),
    # #                 xaxis=dict(
    # #                     tickformat="%Y-%m-%d",
    # #                 ),
    # #                 title=dict(
    # #                     text=f'عمق ماهانه سطح آب چاه مشاهده‌ای {well} (متر)',
    # #                     yanchor="top",
    # #                     y=0.98,
    # #                     xanchor="center",
    # #                     x=0.500
    # #                 ),
    # #                 margin=dict(
    # #                     l=50,
    # #                     r=0,
    # #                     b=30,
    # #                     t=50,
    # #                     pad=0
    # #                 ),
    # #                 legend=dict(
    # #                     yanchor="top",
    # #                     y=0.99,
    # #                     xanchor="left",
    # #                     x=0.01
    # #                 )
    # #             )
                
    # #             fig.update_xaxes(calendar='jalali')
                
    # #             notify = dmc.Notification(
    # #                 id ="notify",
    # #                 title = "",
    # #                 message = [""],
    # #                 color = 'red',
    # #                 action = "hide",
    # #             )
                
    # #             result = [
    # #                 0,
    # #                 fig,
    # #                 False,
    # #                 True,
    # #                 notify
    # #             ]
                
    # #             return result
            
    # #         else:
                
    # #             notify = dmc.Notification(
    # #                 id ="notify",
    # #                 title = "خطا",
    # #                 message = ["چاه مشاهده‌ای انتخاب نشده است!"],
    # #                 color = 'red',
    # #                 action = "show",
    # #             )
                
    # #             result = [
    # #                 0,
    # #                 NO_MATCHING_GRAPH_FOUND,
    # #                 True,
    # #                 False,
    # #                 notify
    # #             ]
                
    # #             return result
            
    # #     else:
            
    # #         notify = dmc.Notification(
    # #             id ="notify",
    # #             title = "",
    # #             message = [""],
    # #             color = 'green',
    # #             action = "hide",
    # #         )
            
    # #         result = [
    # #             0,
    # #             NO_MATCHING_GRAPH_FOUND,
    # #             True,
    # #             False,
    # #             notify
    # #         ]
            
    # #         return result


    # # # -----------------------------------------------------------------------------
    # # # CALLBACK: SHOW GRAPH
    # # # ----------------------------------------------------------------------------- 
    # # @app.callback(
    # #     Output("GRAPH", "figure"),
    # #     Output("ALERTS", "children"),
    # #     Input('STUDY_AREA_SELECT', 'value'),
    # #     Input('AQUIFER_SELECT', 'value'),
    # #     Input('WELL_SELECT', 'value'),
    # # )
    # # def show_graph(
    # #     study_area, aquifer, well
    # # ):
    # #     if study_area is not None and len(study_area) != 0 and\
    # #         aquifer is not None and len(aquifer) != 0 and\
    # #             well is not None and len(well) != 0:
                                        
    # #                 sql = f"SELECT * FROM {TABLE_NAME_INTERPOLATED_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"

    # #                 df = pd.read_sql_query(
    # #                     sql = sql,
    # #                     con = ENGINE_DATA
    # #                 )
                                        
    # #                 if len(df) == 0:
                        
    # #                     notify = dmc.Notification(
    # #                         id ="notify",
    # #                         title = "خطا",
    # #                         message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای یا محدوده مطالعاتی انجام دهید."],
    # #                         color = 'red',
    # #                         action = "show",
    # #                         autoClose=10000
    # #                     )
                        
    # #                     result = [
    # #                         NO_MATCHING_GRAPH_FOUND,
    # #                         notify
    # #                     ]
            
    # #                     return result
                        
                    
    # #                 col_sort = ['MAHDOUDE', 'AQUIFER', 'LOCATION', 'DATE_GREGORIAN']                    
    # #                 df = df.sort_values(by=col_sort).reset_index(drop=True)
                                        
    # #                 fig = go.Figure()
                    
    # #                 fig.add_trace(
    # #                     go.Scatter(
    # #                         x=df['DATE_GREGORIAN'],
    # #                         y=df['WATER_TABLE'],
    # #                         mode='lines+markers',
    # #                         name=f'داده‌های کنترل کیفی شده',
    # #                         marker=dict(
    # #                             color='blue',
    # #                             size=10,
    # #                         ),
    # #                         line=dict(
    # #                             color='black',
    # #                             width=1
    # #                         )  
    # #                     )
    # #                 )
                    
    # #                 tmp = df[df["DESCRIPTION"].str.contains("روش بازسازی")]
                                        
    # #                 fig.add_trace(
    # #                     go.Scatter(
    # #                         x=tmp['DATE_GREGORIAN'],
    # #                         y=tmp['WATER_TABLE'],
    # #                         mode='markers',
    # #                         name=f'داده‌های بازسازی شده',
    # #                         marker=dict(
    # #                             color='red',
    # #                             size=10,
    # #                         ),

    # #                     )
    # #                 )

    # #                 fig.update_layout(
    # #                     hoverlabel=dict(
    # #                         namelength = -1
    # #                     ),
    # #                     yaxis_title="عمق سطح آب - متر",
    # #                     xaxis_title='تاریخ',
    # #                     autosize=False,
    # #                     font=dict(
    # #                         family="Vazir-Regular-FD",
    # #                         size=14,
    # #                         color="RebeccaPurple"
    # #                     ),
    # #                     xaxis=dict(
    # #                         tickformat="%Y-%m-%d",
    # #                     ),
    # #                     title=dict(
    # #                         text=f'عمق ماهانه سطح آب چاه مشاهده‌ای {well} (متر)',
    # #                         yanchor="top",
    # #                         y=0.98,
    # #                         xanchor="center",
    # #                         x=0.500
    # #                     ),
    # #                     margin=dict(
    # #                         l=50,
    # #                         r=0,
    # #                         b=30,
    # #                         t=50,
    # #                         pad=0
    # #                     ),
    # #                     legend=dict(
    # #                         yanchor="top",
    # #                         y=0.99,
    # #                         xanchor="left",
    # #                         x=0.01
    # #                     )
    # #                 )
                    
    # #                 fig.update_xaxes(calendar='jalali')
                    
    # #                 notify = dmc.Notification(
    # #                     id ="notify",
    # #                     title = "",
    # #                     message = [""],
    # #                     color = 'green',
    # #                     action = "hide",
    # #                 )
                    
    # #                 result = [
    # #                     fig,
    # #                     notify
    # #                 ]
            
    # #                 return result

    # #     else:
            
    # #         notify = dmc.Notification(
    # #             id ="notify",
    # #             title = "",
    # #             message = [""],
    # #             color = 'green',
    # #             action = "hide",
    # #         )
            
    # #         result = [
    # #             NO_MATCHING_GRAPH_FOUND,
    # #             notify
    # #         ]
            
    # #         return result


    # # # -----------------------------------------------------------------------------
    # # # CALLBACK: OPTION FOR DROPDOWN WHICH-WELL
    # # # -----------------------------------------------------------------------------  
    # # @app.callback(
    # #     Output('SAVE_WHICH_WELL', 'options'),
    # #     Input('STUDY_AREA_SELECT', 'value'),
    # #     Input('AQUIFER_SELECT', 'value'),
    # #     Input('WELL_SELECT', 'value'),
    # # ) 
    # # def which_well_selected(
    # #     study_area, aquifer, well
    # # ):
    # #     if study_area is not None and len(study_area) != 0 and\
    # #         aquifer is not None and len(aquifer) != 0 and\
    # #             well is not None and len(well) != 0:
                    
    # #                 return [
    # #                     {'label': 'همه چاه‌های مشاهده‌ای', 'value': 0},
    # #                     {'label': f'همه چاه‌های محدوده‌ مطالعاتی {study_area}', 'value': 1},
    # #                     {'label': f'همه چاه‌های آبخوان‌ {aquifer}', 'value': 2},
    # #                     {'label': f'چاه مشاهده‌ای {well}', 'value': 3},
    # #                 ]
                    
    # #     elif study_area is not None and len(study_area) != 0 and\
    # #         aquifer is not None and len(aquifer) != 0:
            
    # #             return [
    # #                 {'label': 'همه چاه‌های مشاهده‌ای', 'value': 0},
    # #                 {'label': f'همه چاه‌های محدوده‌ مطالعاتی {study_area}', 'value': 1},
    # #                 {'label': f'همه چاه‌های آبخوان‌ {aquifer}', 'value': 2},
    # #             ]
                
    # #     elif study_area is not None and len(study_area) != 0:
            
    # #             return [
    # #                 {'label': 'همه چاه‌های مشاهده‌ای', 'value': 0},
    # #                 {'label': f'همه چاه‌های محدوده‌ مطالعاتی {study_area}', 'value': 1},
    # #             ]
                
    # #     else:
            
    # #         return [
    # #             {'label': 'همه چاه‌های مشاهده‌ای', 'value': 0},
    # #         ]


    # # # -----------------------------------------------------------------------------
    # # # CALLBACK: SAVE SYNCDATE DATA
    # # # -----------------------------------------------------------------------------  
    # # @app.callback(
    # #     Output('SAVE_SYNC_DATE_BUTTON', 'n_clicks'),
    # #     Output("ALERTS", "children"),
    # #     Input('SAVE_SYNC_DATE_BUTTON', 'n_clicks'),
    # #     Input('STUDY_AREA_SELECT', 'value'),
    # #     Input('AQUIFER_SELECT', 'value'),
    # #     Input('WELL_SELECT', 'value'),
    # #     Input('SAVE_SYNC_DAY', 'value'),
    # #     Input('SAVE_WHICH_WELL', 'value'),
    # # ) 
    # # def save_syncdate(
    # #     n, study_area, aquifer, well, day, which_well
    # # ):
    # #     if n != 0:
            
    # #         if which_well is not None:
                
    # #             table_exist = find_table(
    # #                 database=POSTGRES_DB_DATA,
    # #                 table=TABLE_NAME_SYNCDATE_DATA,
    # #                 user=POSTGRES_USER_NAME,
    # #                 password=POSTGRES_PASSWORD,
    # #                 host=POSTGRES_HOST,
    # #                 port=POSTGRES_PORT
    # #             )
                
    # #             if which_well == 0:

    # #                 sql = f"SELECT * FROM {TABLE_NAME_INTERPOLATED_DATA}"

    # #                 df = pd.read_sql_query(
    # #                     sql = sql,
    # #                     con = ENGINE_DATA
    # #                 )
                    
    # #                 if len(df) == 0:
                
    # #                     notify = dmc.Notification(
    # #                         id ="notify",
    # #                         title = "خطا",
    # #                         message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی انجام دهید."],
    # #                         color = 'red',
    # #                         action = "show",
    # #                         autoClose=10000
    # #                     )
                        
    # #                     result = [
    # #                         0,
    # #                         notify
    # #                     ]
                        
    # #                     return result
                                            
    # #                 df = df.groupby(
    # #                     by=["MAHDOUDE", "AQUIFER", "LOCATION"]
    # #                 ).apply(lambda x: f_syncdate(
    # #                     df=x,
    # #                     day=day
    # #                 )).reset_index(drop=True)
                    
    # #                 df = df.sort_values(
    # #                     by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
    # #                 )
                    
    # #                 update_table(
    # #                     data=df,
    # #                     table_exist=table_exist,
    # #                     table_name=TABLE_NAME_SYNCDATE_DATA,
    # #                     engine=engine,
    # #                     study_area=None,
    # #                     aquifer=None,
    # #                     well=None,
    # #                 )
                    
    # #                 notify = dmc.Notification(
    # #                     id ="notify",
    # #                     title = "خبر",
    # #                     message = ["تغییرات با موفقیت آپدیت شد!"],
    # #                     color = 'green',
    # #                     action = "show",
    # #                 )
                    
    # #                 result = [
    # #                     0,
    # #                     notify
    # #                 ]
                
    # #                 return result
                
    # #             elif which_well == 1:
                    
    # #                 sql = f"SELECT * FROM {TABLE_NAME_INTERPOLATED_DATA} WHERE \"MAHDOUDE\" = '{study_area}'"

    # #                 df = pd.read_sql_query(
    # #                     sql = sql,
    # #                     con = engine
    # #                 )
                    
    # #                 if len(df) == 0:
                
    # #                     notify = dmc.Notification(
    # #                         id ="notify",
    # #                         title = "خطا",
    # #                         message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی انجام دهید."],
    # #                         color = 'red',
    # #                         action = "show",
    # #                         autoClose=10000
    # #                     )
                        
    # #                     result = [
    # #                         0,
    # #                         notify
    # #                     ]
                        
    # #                     return result
                    
    # #                 df = df.groupby(
    # #                     by=["MAHDOUDE", "AQUIFER", "LOCATION"]
    # #                 ).apply(lambda x: f_syncdate(
    # #                     df=x,
    # #                     day=day
    # #                 )).reset_index(drop=True)
                    
    # #                 df = df.sort_values(
    # #                     by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
    # #                 )
                                        
    # #                 update_table(
    # #                     data=df,
    # #                     table_exist=table_exist,
    # #                     table_name=TABLE_NAME_SYNCDATE_DATA,
    # #                     engine=engine,
    # #                     study_area=study_area,
    # #                     aquifer=None,
    # #                     well=None,
    # #                 )
                    
    # #                 notify = dmc.Notification(
    # #                     id ="notify",
    # #                     title = "خبر",
    # #                     message = ["تغییرات با موفقیت آپدیت شد!"],
    # #                     color = 'green',
    # #                     action = "show",
    # #                 )
                    
    # #                 result = [
    # #                     0,
    # #                     notify
    # #                 ]
                
    # #                 return result
                
    # #             elif which_well == 2:
                    
    # #                 sql = f"SELECT * FROM {TABLE_NAME_INTERPOLATED_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'"

    # #                 df = pd.read_sql_query(
    # #                     sql = sql,
    # #                     con = engine
    # #                 )

    # #                 if len(df) == 0:
                
    # #                     notify = dmc.Notification(
    # #                         id ="notify",
    # #                         title = "خطا",
    # #                         message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی انجام دهید."],
    # #                         color = 'red',
    # #                         action = "show",
    # #                         autoClose=10000
    # #                     )
                        
    # #                     result = [
    # #                         0,
    # #                         notify
    # #                     ]
                        
    # #                     return result
                    
                                            
    # #                 df = df.groupby(
    # #                     by=["MAHDOUDE", "AQUIFER", "LOCATION"]
    # #                 ).apply(lambda x: f_syncdate(
    # #                     df=x,
    # #                     day=day
    # #                 )).reset_index(drop=True)
                    
    # #                 df = df.sort_values(
    # #                     by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
    # #                 )
                                            
    # #                 update_table(
    # #                     data=df,
    # #                     table_exist=table_exist,
    # #                     table_name=TABLE_NAME_SYNCDATE_DATA,
    # #                     engine=engine,
    # #                     study_area=study_area,
    # #                     aquifer=aquifer,
    # #                     well=None,
    # #                 )
                    
    # #                 notify = dmc.Notification(
    # #                     id ="notify",
    # #                     title = "خبر",
    # #                     message = ["تغییرات با موفقیت آپدیت شد!"],
    # #                     color = 'green',
    # #                     action = "show",
    # #                 )
                    
    # #                 result = [
    # #                     0,
    # #                     notify
    # #                 ]
                
    # #                 return result
                
    # #             elif which_well == 3:
                    
    # #                 sql = f"SELECT * FROM {TABLE_NAME_INTERPOLATED_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well}'"

    # #                 df = pd.read_sql_query(
    # #                     sql = sql,
    # #                     con = engine
    # #                 )
                    
    # #                 if len(df) == 0:
                
    # #                     notify = dmc.Notification(
    # #                         id ="notify",
    # #                         title = "خطا",
    # #                         message = ["در پایگاه داده هیچ داده‌ای برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی وجود ندارد! لطفا گام سوم را برای این چاه مشاهده‌ای، آبخوان یا محدوده مطالعاتی انجام دهید."],
    # #                         color = 'red',
    # #                         action = "show",
    # #                         autoClose=10000
    # #                     )
                        
    # #                     result = [
    # #                         0,
    # #                         notify
    # #                     ]
                        
    # #                     return result
                                            
    # #                 df = df.groupby(
    # #                     by=["MAHDOUDE", "AQUIFER", "LOCATION"]
    # #                 ).apply(lambda x: f_syncdate(
    # #                     df=x,
    # #                     day=day
    # #                 )).reset_index(drop=True)
                    
    # #                 df = df.sort_values(
    # #                     by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
    # #                 )
                                            
    # #                 update_table(
    # #                     data=df,
    # #                     table_exist=table_exist,
    # #                     table_name=TABLE_NAME_SYNCDATE_DATA,
    # #                     engine=engine,
    # #                     study_area=study_area,
    # #                     aquifer=aquifer,
    # #                     well=well,
    # #                 )
                    
    # #                 notify = dmc.Notification(
    # #                     id ="notify",
    # #                     title = "خبر",
    # #                     message = ["تغییرات با موفقیت آپدیت شد!"],
    # #                     color = 'green',
    # #                     action = "show",
    # #                 )
                    
    # #                 result = [
    # #                     0,
    # #                     notify
    # #                 ]
                
    # #                 return result
                
    # #             else:
                    
    # #                 pass
                
    # #         else:
                
    # #             notify = dmc.Notification(
    # #                 id ="notify",
    # #                 title = "خطا",
    # #                 message = ["محدوده هماهنگ‌سازی تاریخ انتخاب نشده است!"],
    # #                 color = 'red',
    # #                 action = "show",
    # #             )
                
    # #             result = [
    # #                 0,
    # #                 notify
    # #             ]
                
    # #             return result
        
    # #     else:
            
    # #         notify = dmc.Notification(
    # #             id ="notify",
    # #             title = "",
    # #             message = [""],
    # #             color = 'green',
    # #             action = "hide",
    # #         )
            
    # #         result = [
    # #             0,
    # #             notify
    # #         ]
            
    # #         return result