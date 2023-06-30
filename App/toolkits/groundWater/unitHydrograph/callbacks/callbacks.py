import json
import itertools
import tempfile
from threading import local
import numpy as np
import pandas as pd
import geopandas as gpd
import psycopg2
import statistics
from geoalchemy2 import Geometry, WKTElement
from dash import no_update, dcc, dash_table
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
from . import *


def toolkits__groundWater__unitHydrograph__callbacks(app):
    
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
        Output('WELL_SELECT', 'value'),
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
                        sorted(well_data),
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
                        None,
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
                None,
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
    #     Output('STORAGE_COEFFICIENT', 'value'),      
    #     Input('STUDY_AREA_SELECT', 'value'),
    #     Input('AQUIFER_SELECT', 'value'),
    #     Input('WELL_SELECT', 'value'),
    #     Input('STORAGE_COEFFICIENT', 'value'), 
    # )
    # def update_dropdown_list(
    #     study_area, aquifer, well, sc
    # ):
    #     if (study_area is not None and len(study_area) != 0) and\
    #         (aquifer is None or len(aquifer) == 0) and\
    #             (well is not None and len(well) != 0):
            
    #         result = [
    #             no_update,
    #             [],
    #             [],
    #             None
    #         ]
            
    #         return result
        
    #     elif (study_area is None or len(study_area) == 0) and\
    #         (aquifer is not None and len(aquifer) != 0) and\
    #             (well is not None and len(well) != 0):
            
    #         result = [
    #             [],
    #             [],
    #             [],
    #             None
    #         ]
            
    #         return result
        
    #     else:
            
    #         result = [
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
                                       
                    df_study_area = gpd.GeoDataFrame.from_postgis(
                        sql=f"SELECT * FROM {DB_LAYERS_TABLE_MAHDOUDE} WHERE \"MAHDOUDE\" = '{study_area}'",
                        con=ENGINE_LAYERS,
                        geom_col="geometry"
                    )
                    
                    df_study_area_json = json.loads(df_study_area.to_json())
                    
                    for feature in df_study_area_json["features"]:
                        feature['id'] = feature['properties']['MAHDOUDE']
                    
                    #* AQUIFER:
                                        
                    df_aquifer = gpd.GeoDataFrame.from_postgis(
                        sql=f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'",
                        con=ENGINE_LAYERS,
                        geom_col="geometry"
                    )
                    
                    df_aquifer_json = json.loads(df_aquifer.to_json())
                    
                    for feature in df_aquifer_json["features"]:
                        feature['id'] = feature['properties']['AQUIFER']
                    
                    #* SELECTED WELL:
                    
                    if len(well) == 1:
                        sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well[0]}'"
                    else:
                        sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" IN {*well,}"
                    
                    df_well = gpd.GeoDataFrame.from_postgis(
                        sql=sql,
                        con=ENGINE_LAYERS,
                        geom_col="geometry"
                    )
                                        
                    #* ALL WELL:
                                        
                    df_all_well = gpd.GeoDataFrame.from_postgis(
                        sql=f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}'",
                        con=ENGINE_LAYERS,
                        geom_col="geometry"
                    )
                    
                    df_well_non_selected = df_all_well[~df_all_well['LOCATION'].isin(well)]
                                        
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
                            lat=df_well.Y,
                            lon=df_well.X,
                            mode='markers',
                            marker=go.scattermapbox.Marker(size=12, color="green"),
                            text=df_well["LOCATION"],
                            hoverinfo='text',
                            hovertemplate='<span style="color:white;">%{text}</span><extra></extra>'
                        )
                    )
                    
                    if len(df_well_non_selected) != 0:
                    
                        fig.add_trace(
                            go.Scattermapbox(
                                lat=df_well_non_selected.Y,
                                lon=df_well_non_selected.X,
                                mode='markers',
                                marker=go.scattermapbox.Marker(size=12, color="red"),
                                text=df_well_non_selected["LOCATION"],
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
                    
                    fig.update_layout(
                        mapbox_accesstoken=MAPBOX_TOKEN
                    )
                    
                    return fig

        else:
            
            return BASE_MAP
        
    # -----------------------------------------------------------------------------
    # CALLBACK: STORAGE COEFFICIENT
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('STORAGE_COEFFICIENT', 'placeholder'),
        Output('STORAGE_COEFFICIENT', 'value'),
        State('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
    )
    def storage_coefficient(
        study_area, aquifer
    ):
        if (study_area is not None and len(study_area) != 0) and\
            (aquifer is not None and len(aquifer) != 0):
                
                try:
                    sc = STORAGE_COEFFICIENT[
                        (STORAGE_COEFFICIENT["MAHDOUDE"] == study_area) & (STORAGE_COEFFICIENT["AQUIFER"] == aquifer)
                    ]

                    result = [
                        f"آبخوان {aquifer}",
                        sc["SC"].values[0]
                    ]
                    
                    return result
                except:
                    result = [
                        f"آبخوان ...",
                        None
                    ]
            
                    return result
        
        else:
        
            result = [
                f"آبخوان ...",
                None
            ]
            
            return result
    
    
    # -----------------------------------------------------------------------------
    # CALLBACK: CALCULATE UNIT HYDROGRAPH
    # -----------------------------------------------------------------------------
    @app.callback(
        Output('CALCULATE_UNIT_HYDROGRAPH', 'n_clicks'),
        Output("ALERTS", "children"),
        Output('INTERVAL', 'n_intervals'),
        Output('SELECT_DATE_THIESSEN', 'value'),
        Output('DIV_SELECT_DATE_THIESSEN', 'hidden'),
        Output('UNIT_HYDROGRAPH_GRAPH', 'children'),        
        Input('CALCULATE_UNIT_HYDROGRAPH', 'n_clicks'),
        Input('CRS', 'value'),        
        State('STUDY_AREA_SELECT', 'value'),
        State('AQUIFER_SELECT', 'value'),
        State('WELL_SELECT', 'value'),
        State('STORAGE_COEFFICIENT', 'value'),
        State('UNIT_HYDROGRAPH_METHOD', 'value'),
    )
    def calculate_unit_hydrograph(
        n, epsg, study_area, aquifer, well, sc, methods
    ):
        if n != 0:
            
            if (study_area is not None and len(study_area) != 0) and (aquifer is not None and len(aquifer) != 0) and (well is not None and len(well) != 0):
                
                if sc is not None:
                    
                    if methods is not None and len(methods) != 0:
                        
                        #* GEODATAFRAME AQUIFER:
                        sql = f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}';"
                        
                        gdf_db_layers_table_aquifer = gpd.GeoDataFrame.from_postgis(
                            sql=sql,
                            con=ENGINE_LAYERS,
                            geom_col="geometry"
                        )
                        
                        #* GEODATAFRAME SELECTED WELL:
                        if len(well) == 1:
                            sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well[0]}';"
                        else:
                            sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" IN {*well,};"
                        
                        gdf_db_layers_table_well = gpd.GeoDataFrame.from_postgis(
                            sql=sql,
                            con=ENGINE_LAYERS,
                            geom_col="geometry"
                        )
                        
                        #* DATAFRAME WATER LEVEL DATA:
                        if len(well) == 1:
                            sql = f"SELECT * FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well[0]}';"
                        else:
                            sql = f"SELECT * FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" IN {*well,};"
                        
                        df_db_data_table_data = pd.read_sql_query(
                            sql=sql,
                            con=ENGINE_DATA
                        ).sort_values(
                            ["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                        ).reset_index(drop=True)
                        
                        #* ADD STORAGE COEFFICIENTS TO DATAFRAME WATER LEVEL:
                        df_db_data_table_data["STORAGE_COEFFICIENT"] = sc
                        
                        # WARNING: FOR DIFFERENT DAY OF MONTH, THIS METHOD MUST BE MODIFY.
                        
                        result = pd.DataFrame(
                            columns=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                        )
                        
                        for m in methods:
                            
                            if m in ["AM", "GM", "HM", "ME"]:
                                
                                st = {
                                    "AM": statistics.mean,
                                    "GM": statistics.geometric_mean,
                                    "HM": statistics.harmonic_mean,
                                    "ME": statistics.median,
                                }
                                
                                tmp = df_db_data_table_data[
                                    ["MAHDOUDE", "AQUIFER", "LOCATION", "YEAR_PERSIAN", "MONTH_PERSIAN", "WATER_LEVEL"]
                                ]
                                                                
                                tmp = tmp.groupby(
                                    by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).agg({
                                    "WATER_LEVEL": st[m]
                                }).reset_index()
                                
                                tmp = tmp.sort_values(
                                    by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).reset_index(drop=True).rename(columns={"WATER_LEVEL" : f"UNIT_HYDROGRAPH_{m}"})
                                
                                
                                result = result.merge(
                                    tmp, 
                                    how="outer", 
                                    on=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).sort_values(
                                    by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).reset_index(drop=True)
                                
                            if m == "TWA":
                                
                                tmp_data = df_db_data_table_data[
                                    ["MAHDOUDE", "AQUIFER", "LOCATION", "YEAR_PERSIAN", "MONTH_PERSIAN", "WATER_LEVEL", "STORAGE_COEFFICIENT"]
                                ]
                                
                                gdf_db_layers_table_well = gdf_db_layers_table_well.to_crs(epsg=epsg)
                                gdf_db_layers_table_aquifer = gdf_db_layers_table_aquifer.to_crs(epsg=epsg)
                                
                                tmp_thissen = tmp_data.groupby(
                                    by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                    ).apply(
                                        lambda x: calculate_thiessen_polygons(
                                            data=x,
                                            para="WATER_LEVEL",
                                            point=gdf_db_layers_table_well,
                                            point_name="LOCATION",
                                            limit=gdf_db_layers_table_aquifer
                                        )
                                    ).reset_index()
                                
                                tmp_thissen = tmp_thissen[['MAHDOUDE', 'AQUIFER', 'LOCATION', 'YEAR_PERSIAN', 'MONTH_PERSIAN', 'THISSEN_POINT', 'THISSEN_LIMIT', 'geometry']]
                                
                                tmp_thissen = tmp_thissen.rename(
                                    columns={
                                        "THISSEN_POINT" : "THISSEN_LOCATION",
                                        "THISSEN_LIMIT" : "THISSEN_AQUIFER",
                                    }
                                )
                                
                                tmp_thissen = tmp_thissen.to_crs(epsg=4326)
                                
                                tmp_thissen.to_postgis(
                                    name=DB_LAYERS_TABLE_TEMPORARY,
                                    con=ENGINE_LAYERS,
                                    if_exists='replace',
                                    index=False,
                                    dtype={'geometry': Geometry(srid= 4326)}
                                )
                                
                                tmp = tmp_data.merge(
                                    tmp_thissen, 
                                    how="left", 
                                    on=["MAHDOUDE", "AQUIFER", "LOCATION", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).sort_values(
                                    ["MAHDOUDE", "AQUIFER", "LOCATION", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).reset_index(drop=True)
                                
                                tmp['UNIT_HYDROGRAPH_TWA'] = (tmp["WATER_LEVEL"] * tmp['THISSEN_LOCATION']) / tmp['THISSEN_AQUIFER']
                                
                                tmp['STORAGE_COEFFICIENT_AQUIFER'] = (tmp["STORAGE_COEFFICIENT"] * tmp['THISSEN_LOCATION']) / tmp['THISSEN_AQUIFER']

                                tmp = tmp.groupby(
                                    by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).agg({
                                    "UNIT_HYDROGRAPH_TWA": 'sum',
                                    "STORAGE_COEFFICIENT_AQUIFER": 'sum',
                                    "THISSEN_AQUIFER": 'mean', 
                                }).reset_index()
                                
                                tmp = tmp.sort_values(
                                    by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).reset_index(drop=True)
                                
                                result = result.merge(
                                    tmp[['MAHDOUDE', 'AQUIFER', 'YEAR_PERSIAN', 'MONTH_PERSIAN', 'UNIT_HYDROGRAPH_TWA', 'THISSEN_AQUIFER', "STORAGE_COEFFICIENT_AQUIFER"]], 
                                    how="outer", 
                                    on=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).sort_values(
                                    by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).reset_index(drop=True)
                                
                                #* TWA ADJUSTED
                                
                                median_diff = tmp_data.groupby(by=["MAHDOUDE", "AQUIFER", "LOCATION"])["WATER_LEVEL"].diff().reset_index(drop=True).abs().median()
                                
                                df_thiessen_change = tmp_data.groupby(by=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"])["LOCATION"]\
                                    .apply(list)\
                                        .reset_index(name='LOCATION_LIST').sort_values(["YEAR_PERSIAN", "MONTH_PERSIAN"])
                                                                                                
                                df_thiessen_change_aquifer = df_thiessen_change.groupby(by=["MAHDOUDE", "AQUIFER"])\
                                    .apply(check_thiessen_change).reset_index(drop=True)
                                                                
                                result = result.merge(
                                    right=df_thiessen_change_aquifer[["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN", "THISSEN_CHANGE"]],
                                    how='left',
                                    on=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                ).sort_values(["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"])
                                                
                                tmp = result.copy()
                                tmp['DELTA'] = tmp['UNIT_HYDROGRAPH_TWA'].diff().fillna(0)
                                tmp['UNIT_HYDROGRAPH_TWA_ADJ'] = tmp['UNIT_HYDROGRAPH_TWA']
                                tmp["YM_PERSIAN"] = tmp["YEAR_PERSIAN"] + "-" + tmp["MONTH_PERSIAN"]
                                n = tmp[tmp["THISSEN_CHANGE"]]["YM_PERSIAN"].tolist()
                                
                                if len(n) > 0:                    
                                    for dt in n:                
                                        delta = tmp.loc[tmp["YM_PERSIAN"] == dt, "DELTA"].reset_index()["DELTA"][0]
                                        if delta >= 0:
                                            if abs(delta) > abs(median_diff):
                                                delta = delta - median_diff
                                            else:
                                                delta = 0
                                        else:
                                            if abs(delta) > abs(median_diff):
                                                delta = delta + median_diff
                                            else:
                                                delta = 0
                                            
                                        ix = tmp.loc[tmp["YM_PERSIAN"] == dt, "DELTA"].reset_index()["index"][0]
                                        tmp['TMP'] = tmp['UNIT_HYDROGRAPH_TWA_ADJ']
                                        
                                        for i in range(ix):                    
                                            tmp['TMP'][i] = tmp['UNIT_HYDROGRAPH_TWA_ADJ'][i] + delta                    
                                        tmp['UNIT_HYDROGRAPH_TWA_ADJ'] = tmp['TMP']
                                
                                result = result.merge(
                                    right=tmp[["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN", "UNIT_HYDROGRAPH_TWA_ADJ"]],
                                    how='left',
                                    on=["MAHDOUDE", "AQUIFER", "YEAR_PERSIAN", "MONTH_PERSIAN"]
                                )

                        result["YM_PERSIAN"] = result["YEAR_PERSIAN"] + "-" + result["MONTH_PERSIAN"]
                        result["DAY_PERSIAN"] = "01"                        
                        cols_p = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
                        cols_g = ['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']                       
                        result[cols_p] = result[cols_p].apply(pd.to_numeric, errors='coerce')
                        result[cols_p] = result[cols_p].astype(pd.Int64Dtype())
                        date_persian, date_gregorian = np.vectorize(check_persian_date_ymd)(result.YEAR_PERSIAN, result.MONTH_PERSIAN, result.DAY_PERSIAN)
                        result["DATE_PERSIAN"] = list(date_persian)
                        result["DATE_GREGORIAN"] = list(date_gregorian)
                        result[cols_p] = result['DATE_PERSIAN'].str.split('-', 2, expand=True)
                        result[cols_g] = result['DATE_GREGORIAN'].astype(str).str.split('-', 2, expand=True)
                        result["YEAR_PERSIAN"] = result["YEAR_PERSIAN"].astype(str).str.zfill(4)
                        result["MONTH_PERSIAN"] = result["MONTH_PERSIAN"].astype(str).str.zfill(2)
                        result["DAY_PERSIAN"] = result["DAY_PERSIAN"].astype(str).str.zfill(2)
                        result["YEAR_GREGORIAN"] = result["YEAR_GREGORIAN"].str.zfill(4)
                        result["MONTH_GREGORIAN"] = result["MONTH_GREGORIAN"].str.zfill(2)
                        result["DAY_GREGORIAN"] = result["DAY_GREGORIAN"].str.zfill(2)
                        result['DATE_PERSIAN'] = result["YEAR_PERSIAN"] + "-" + result["MONTH_PERSIAN"] + "-" + result["DAY_PERSIAN"]
                        result['DATE_GREGORIAN'] = result["YEAR_GREGORIAN"] + "-" + result["MONTH_GREGORIAN"] + "-" + result["DAY_GREGORIAN"]
                        result["DATE_GREGORIAN"] = result["DATE_GREGORIAN"].apply(pd.to_datetime)
                        
                        result.to_sql(
                            name=DB_DATA_TABLE_TEMPORARY,
                            con=ENGINE_DATA,
                            if_exists='replace',
                            index=False
                        )

                        notify = dmc.Notification(
                            id ="notify",
                            title = "خبر",
                            message = ["محاسبات با موفقیت انجام شد!"],
                            color = 'green',
                            action = "show"
                        )
                        
                        result = [
                            0,
                            notify,
                            0,
                            None,
                            True,
                            dcc.Graph(
                                figure=NO_MATCHING_GRAPH_FOUND
                            )
                        ]
                        
                        return result
                    
                    else:
                        
                        notify = dmc.Notification(
                            id ="notify",
                            title = "خطا",
                            message = ["حداقل یک روش برای محاسبه هیدروگراف واحد آبخوان باید انتخاب گردد!"],
                            color = 'red',
                            action = "show"
                        )
                    
                        result = [
                            0,
                            notify,
                            1,
                            None,
                            True,
                            dcc.Graph(
                                figure=NO_MATCHING_GRAPH_FOUND
                            )
                        ]
                    
                        return result
                
                else:
            
                    notify = dmc.Notification(
                        id ="notify",
                        title = "خطا",
                        message = ["ضریب ذخیره آبخوان وارد نشده است!"],
                        color = 'red',
                        action = "show"
                    )
                
                    result = [
                        0,
                        notify,
                        1,
                        None,
                        True,
                        dcc.Graph(
                            figure=NO_MATCHING_GRAPH_FOUND
                        )
                    ]
                
                    return result
            
            else:
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["محدوده مطالعاتی یا آبخوان یا چاه‌های مشاهده‌ای انتخاب نشده‌اند!"],
                    color = 'red',
                    action = "show"
                )
            
                result = [
                    0,
                    notify,
                    1,
                    None,
                    True,
                    dcc.Graph(
                        figure=NO_MATCHING_GRAPH_FOUND
                    )
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
                0,
                notify,
                1,
                no_update,
                no_update,
                no_update,
            ]
            
            return result
    
    # -----------------------------------------------------------------------------
    # CALLBACK: GRAPH
    # -----------------------------------------------------------------------------  
    @app.callback(
        Output('SHOW_UNIT_HYDROGRAPH', 'n_clicks'),        
        Output('UNIT_HYDROGRAPH_GRAPH', 'children'),       
        Input('SHOW_UNIT_HYDROGRAPH', 'n_clicks'),
    ) 
    def graph(
        n
    ):
        if n != 0:
                
            sql = f"SELECT * FROM {DB_DATA_TABLE_TEMPORARY}"

            df = pd.read_sql_query(
                sql = sql,
                con = ENGINE_DATA
            )
            
            df = df.sort_values(
                by=["MAHDOUDE", "AQUIFER", "DATE_GREGORIAN"]
            ).reset_index(drop=True)
            
            fig = go.Figure()
            
            if "UNIT_HYDROGRAPH_AM" in df.columns:
                
                fig.add_trace(
                    go.Scatter(
                        x=df["DATE_GREGORIAN"],
                        y=df["UNIT_HYDROGRAPH_AM"],
                        name="Arithmetic Mean",
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
            
            if "UNIT_HYDROGRAPH_GM" in df.columns:
                
                fig.add_trace(
                    go.Scatter(
                        x=df["DATE_GREGORIAN"],
                        y=df["UNIT_HYDROGRAPH_GM"],
                        name="Geometric Mean",
                        mode="lines+markers",
                        marker=dict(
                            color="red",
                            size=10,
                        ),
                        line=dict(
                            color="red",
                            width=1
                        ),
                        line_shape='spline'
                    )
                )
            
            if "UNIT_HYDROGRAPH_HM" in df.columns:
                
                fig.add_trace(
                    go.Scatter(
                        x=df["DATE_GREGORIAN"],
                        y=df["UNIT_HYDROGRAPH_HM"],
                        name="Harmonic Mean",
                        mode="lines+markers",
                        marker=dict(
                            color="green",
                            size=10,
                        ),
                        line=dict(
                            color="green",
                            width=1
                        ),
                        line_shape='spline'
                    )
                )
            
            if "UNIT_HYDROGRAPH_ME" in df.columns:
                
                fig.add_trace(
                    go.Scatter(
                        x=df["DATE_GREGORIAN"],
                        y=df["UNIT_HYDROGRAPH_ME"],
                        name="Median",
                        mode="lines+markers",
                        marker=dict(
                            color="brown",
                            size=10,
                        ),
                        line=dict(
                            color="brown",
                            width=1
                        ),
                        line_shape='spline'
                    )
                )
            
            if "UNIT_HYDROGRAPH_TWA" in df.columns:
                
                fig.add_trace(
                    go.Scatter(
                        x=df["DATE_GREGORIAN"],
                        y=df["UNIT_HYDROGRAPH_TWA"],
                        name="Thiessen Weighted Average",
                        mode="lines+markers",
                        marker=dict(
                            color="black",
                            size=10,
                        ),
                        line=dict(
                            color="black",
                            width=1
                        ),
                        line_shape='spline'
                    )
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=df["DATE_GREGORIAN"],
                        y=df["UNIT_HYDROGRAPH_TWA_ADJ"],
                        name="Adjusted Thiessen Weighted Average",
                        mode="lines+markers",
                        marker=dict(
                            color="gray",
                            size=10,
                        ),
                        line=dict(
                            color="gray",
                            width=1
                        ),
                        line_shape='spline'
                    )
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=df[df["THISSEN_CHANGE"]]["DATE_GREGORIAN"],
                        y=df[df["THISSEN_CHANGE"]]["UNIT_HYDROGRAPH_TWA"],
                        name="Thiessen Changed",
                        mode="markers",
                        marker=dict(
                            color="orange",
                            size=16,
                            symbol='x'
                        ),
                        line_shape='spline'
                    )
                )

            fig.update_layout(
                hoverlabel=dict(
                    namelength = -1
                ),
                # yaxis_title="تراز سطح آب - متر",
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
                    text=f"تراز ماهانه سطح آب آبخوان {df['AQUIFER'].unique()[0]} بر حسب متر",
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
                    # yanchor="top",
                    # y=0.99,
                    # xanchor="left",
                    # x=0.01
                    orientation="h",
                    yanchor="bottom",
                    y=0.01,
                    xanchor="center",
                    x=0.5
                )
            )
            
            fig.update_xaxes(
                calendar='jalali',
                tickformat="%Y-%m",
            )
            
            result = [
                0,
                dcc.Graph(
                    figure=fig
                ),
            ]
            
            return result
        
        else:
            
            result = [
                0,
                dcc.Graph(
                    figure=NO_MATCHING_GRAPH_FOUND
                ),
            ]
            
            return result
            

    # -----------------------------------------------------------------------------
    # CALLBACK: GRAPH
    # -----------------------------------------------------------------------------  
    @app.callback(        
        Output('SHOW_THIESSEN_MAP', 'n_clicks'),
        Output('DIV_SELECT_DATE_THIESSEN', 'hidden'), 
        Output('SELECT_DATE_THIESSEN', 'options'),         
        Output('SELECT_DATE_THIESSEN', 'value'),
        Output('MAP_THIESSEN', 'figure'),
        Output('THIESSEN_TABLE', 'children'),
        Input('SHOW_THIESSEN_MAP', 'n_clicks'),
        Input('SELECT_DATE_THIESSEN', 'value'),
    ) 
    def thiessen_map(
        n, date_thiessen
    ):
        if n != 0:
            
            # SECTION: SELECT DATE THIESSEN
            sql_thiessen = f"SELECT * FROM {DB_LAYERS_TABLE_TEMPORARY}"
                    
            df_thiessen = gpd.GeoDataFrame.from_postgis(
                sql=sql_thiessen,
                con=ENGINE_LAYERS,
                geom_col="geometry"
            )
            
            df_thiessen["YM_PERSIAN"] = df_thiessen["YEAR_PERSIAN"] + "-" + df_thiessen["MONTH_PERSIAN"]
            
            dt = sorted(list(df_thiessen["YM_PERSIAN"].unique()))

            df_thiessen = df_thiessen[df_thiessen["YM_PERSIAN"] == dt[0]]
            
            df_thiessen["PERCENTAGE"] = (df_thiessen["THISSEN_LOCATION"] * 100) / df_thiessen["THISSEN_AQUIFER"]
            df_thiessen["PERCENTAGE"] = df_thiessen["PERCENTAGE"].round(1)
                                    
            map_thiessen = px.choropleth_mapbox(
                data_frame=df_thiessen,
                geojson=df_thiessen.geometry,
                locations=df_thiessen.index,
                color="PERCENTAGE",
                color_continuous_scale="RdYlGn_r",
                hover_name="LOCATION",
                hover_data={"LOCATION": False},
                opacity=0.4,
            )
            
            map_thiessen.update_coloraxes(showscale=False)
    
            map_thiessen.update_layout(
                mapbox = {
                    'style': "stamen-terrain",
                    'zoom': 8,
                    'center': {
                        'lat': df_thiessen.centroid.y.mean(),
                        'lon': df_thiessen.centroid.x.mean(),
                    },
                },
                autosize=True,
                showlegend = False,
                hovermode='closest',
                margin = {'l':0, 'r':0, 'b':0, 't':0},
            )
            
            map_thiessen.update_layout(
                mapbox_accesstoken=MAPBOX_TOKEN
            )
            
            # DATA
            study_area = df_thiessen["MAHDOUDE"].unique()[0]
            aquifer = df_thiessen["AQUIFER"].unique()[0]
            well = list(df_thiessen["LOCATION"].unique())
            year = dt[0][0:4]
            month = dt[0][5:]
            
            sql_well = f"SELECT DISTINCT \"LOCATION\" FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}';"
            
            well_unique = pd.read_sql_query(
                sql=sql_well,
                con=ENGINE_DATA
            )
             
            if len(well) == 1:
                sql = f"SELECT * FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well[0]}' AND \"YEAR_PERSIAN\" = '{year}' AND \"MONTH_PERSIAN\" = '{month}';"
            else:           
                sql = f"SELECT * FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" IN {*well,} AND \"YEAR_PERSIAN\" = '{year}' AND \"MONTH_PERSIAN\" = '{month}';"
            
            df_water_level = pd.read_sql_query(
                sql=sql,
                con=ENGINE_DATA
            )
            
            df_water_level = df_water_level[["MAHDOUDE", "AQUIFER", "LOCATION", "WATER_TABLE", "WATER_LEVEL"]].merge(
                df_thiessen[["MAHDOUDE", "AQUIFER", "LOCATION", "THISSEN_LOCATION", "THISSEN_AQUIFER"]],
                on=["MAHDOUDE", "AQUIFER", "LOCATION"],
                how="outer"
            )
            
            df_water_level["THISSEN"] = df_water_level["THISSEN_LOCATION"] / df_water_level["THISSEN_AQUIFER"]
            
            df_water_level["THISSEN"] = df_water_level["THISSEN"].round(2)
            
            df_water_level["HYDROGRAPH"] = df_water_level["THISSEN"] * df_water_level["WATER_LEVEL"]
            
            df_water_level["HYDROGRAPH"] = df_water_level["HYDROGRAPH"].round(1)
            
            df_water_level["WATER_LEVEL"] = df_water_level["WATER_LEVEL"].round(1)
            
            df_water_level["WATER_TABLE"] = df_water_level["WATER_TABLE"].round(1)
            
            df_water_level = df_water_level.drop(['MAHDOUDE', 'AQUIFER', 'THISSEN_LOCATION', 'THISSEN_AQUIFER'], axis=1)
            
            df_water_level = df_water_level.merge(
                right=well_unique,
                on="LOCATION",
                how="right"
            )
                        
            df_water_level = df_water_level.sort_values(by=['HYDROGRAPH'], ascending=False)
            
            table_content = dash_table.DataTable(
                columns=[
                    {"name": i, "id": i} for i in df_water_level.columns
                ],
                data=df_water_level.to_dict('records'),
                page_size=10,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                style_as_list_view=True,
                style_table={
                    # 'overflowX': 'auto',
                    'overflowY': 'auto',
                    'direction': 'rtl',
                },
                style_cell={
                    'font-family': "Vazir-Regular-FD",
                    'border': '1px solid grey',
                    'font-size': '16px',
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
                ] + [
                    {
                        'if': {
                            'filter_query': '{HYDROGRAPH} is blank',
                        },
                        'backgroundColor': '#FF4136',
                        'color': 'white'
                    } for col in df_water_level.columns
                ],
            )
            
            result = [
                0, 
                False,
                [{'label': i, 'value': i} for i in dt],
                dt[0],
                map_thiessen,
                table_content,
            ]
            
            return result
        
        elif date_thiessen is not None:
            
            # SECTION: SELECT DATE THIESSEN
            sql_thiessen = f"SELECT * FROM {DB_LAYERS_TABLE_TEMPORARY}"
                    
            df_thiessen = gpd.GeoDataFrame.from_postgis(
                sql=sql_thiessen,
                con=ENGINE_LAYERS,
                geom_col="geometry"
            )
            
            df_thiessen["YM_PERSIAN"] = df_thiessen["YEAR_PERSIAN"] + "-" + df_thiessen["MONTH_PERSIAN"]
            
            dt = sorted(list(df_thiessen["YM_PERSIAN"].unique()))

            df_thiessen = df_thiessen[df_thiessen["YM_PERSIAN"] == date_thiessen]
            
            df_thiessen["PERCENTAGE"] = (df_thiessen["THISSEN_LOCATION"] * 100) / df_thiessen["THISSEN_AQUIFER"]
            df_thiessen["PERCENTAGE"] = df_thiessen["PERCENTAGE"].round(1)
                        
            map_thiessen = px.choropleth_mapbox(
                data_frame=df_thiessen,
                geojson=df_thiessen.geometry,
                locations=df_thiessen.index,
                color="PERCENTAGE",
                color_continuous_scale="RdYlGn_r",
                hover_name="LOCATION",
                hover_data={"LOCATION": False},
                opacity=0.4,
            )
            
            map_thiessen.update_coloraxes(showscale=False)
    
            map_thiessen.update_layout(
                mapbox = {
                    'style': "stamen-terrain",
                    'zoom': 8,
                    'center': {
                        'lat': df_thiessen.centroid.y.mean(),
                        'lon': df_thiessen.centroid.x.mean(),
                    },
                },
                showlegend = False,
                hovermode='closest',
                margin = {'l':0, 'r':0, 'b':0, 't':0}
            )
            
            map_thiessen.update_layout(
                mapbox_accesstoken=MAPBOX_TOKEN
            )
            
            
            # DATA
            study_area = df_thiessen["MAHDOUDE"].unique()[0]
            aquifer = df_thiessen["AQUIFER"].unique()[0]
            well = list(df_thiessen["LOCATION"].unique())
            year = date_thiessen[0:4]
            month = date_thiessen[5:]
            
            sql_well = f"SELECT DISTINCT \"LOCATION\" FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}';"
            
            well_unique = pd.read_sql_query(
                sql=sql_well,
                con=ENGINE_DATA
            )
            
            if len(well) == 1:
                sql = f"SELECT * FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" = '{well[0]}' AND \"YEAR_PERSIAN\" = '{year}' AND \"MONTH_PERSIAN\" = '{month}';"
            else:            
                sql = f"SELECT * FROM {DB_DATA_TABLE_DATA} WHERE \"MAHDOUDE\" = '{study_area}' AND \"AQUIFER\" = '{aquifer}' AND \"LOCATION\" IN {*well,} AND \"YEAR_PERSIAN\" = '{year}' AND \"MONTH_PERSIAN\" = '{month}';"
            
            df_water_level = pd.read_sql_query(
                sql=sql,
                con=ENGINE_DATA
            )
            
            df_water_level = df_water_level[["MAHDOUDE", "AQUIFER", "LOCATION", "WATER_TABLE", "WATER_LEVEL"]].merge(
                df_thiessen[["MAHDOUDE", "AQUIFER", "LOCATION", "THISSEN_LOCATION", "THISSEN_AQUIFER"]],
                on=["MAHDOUDE", "AQUIFER", "LOCATION"],
                how="outer"
            )
            
            df_water_level["THISSEN"] = df_water_level["THISSEN_LOCATION"] / df_water_level["THISSEN_AQUIFER"]
            
            df_water_level["THISSEN"] = df_water_level["THISSEN"].round(2)
            
            df_water_level["HYDROGRAPH"] = df_water_level["THISSEN"] * df_water_level["WATER_LEVEL"]
            
            df_water_level["HYDROGRAPH"] = df_water_level["HYDROGRAPH"].round(1)
            
            df_water_level["WATER_LEVEL"] = df_water_level["WATER_LEVEL"].round(1)
            
            df_water_level["WATER_TABLE"] = df_water_level["WATER_TABLE"].round(1)
            
            df_water_level = df_water_level.drop(['MAHDOUDE', 'AQUIFER', 'THISSEN_LOCATION', 'THISSEN_AQUIFER'], axis=1)
            
            df_water_level = df_water_level.merge(
                right=well_unique,
                on="LOCATION",
                how="right"
            )
            
            df_water_level = df_water_level.sort_values(by=['HYDROGRAPH'], ascending=False)
                        
            table_content = dash_table.DataTable(
                columns=[
                    {"name": i, "id": i} for i in df_water_level.columns
                ],
                data=df_water_level.to_dict('records'),
                page_size=10,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                style_as_list_view=True,
                style_table={
                    # 'overflowX': 'auto',
                    'overflowY': 'auto',
                    'direction': 'rtl',
                },
                style_cell={
                    'font-family': "Vazir-Regular-FD",
                    'border': '1px solid grey',
                    'font-size': '16px',
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
                ] + [
                    {
                        'if': {
                            'filter_query': '{HYDROGRAPH} is blank',
                        },
                        'backgroundColor': '#FF4136',
                        'color': 'white'
                    } for col in df_water_level.columns
                ],
            )
            
            
            result = [
                0, 
                False,
                no_update,
                no_update,
                map_thiessen,
                table_content,
            ]
            
            return result
            
        else:
            
            result = [
                0, 
                True,
                [{}],
                None,
                NO_MATCHING_MAP_FOUND,
                dcc.Graph(
                    figure=NO_MATCHING_TABLE_FOUND
                ),
            ]
            
            return result
        

    # -----------------------------------------------------------------------------
    # CALLBACK: SAVE UNIT HYDROGRAPH
    # -----------------------------------------------------------------------------  
    @app.callback(
        Output('SAVE_UNIT_HYDROGRAPH', 'n_clicks'),
        Output("ALERTS", "children"),       
        Input('SAVE_UNIT_HYDROGRAPH', 'n_clicks'),
    ) 
    def save_unit_hydrograph(
        n,
    ):
        if n != 0:
            
            table_exist = find_table(
                database=POSTGRES_DB_DATA,
                table=DB_DATA_TABLE_TEMPORARY,
                user=POSTGRES_USER_NAME,
                password=POSTGRES_PASSWORD,
                host=POSTGRES_HOST,
                port=POSTGRES_PORT
            )
            
            if table_exist:
            
                sql = f"SELECT * FROM {DB_DATA_TABLE_TEMPORARY}"

                df = pd.read_sql_query(
                    sql = sql,
                    con = ENGINE_DATA
                )
            
                df = df.sort_values(
                    by=["MAHDOUDE", "AQUIFER", "DATE_GREGORIAN"]
                ).reset_index(drop=True)
                
                table_exist = find_table(
                    database=POSTGRES_DB_DATA,
                    table=DB_DATA_TABLE_HYDROGRAPH,
                    user=POSTGRES_USER_NAME,
                    password=POSTGRES_PASSWORD,
                    host=POSTGRES_HOST,
                    port=POSTGRES_PORT
                )
                
                if table_exist:
                    
                    study_area = df["MAHDOUDE"].unique()[0]
                    aquifer = df["AQUIFER"].unique()[0]
                    
                    data_exist = pd.read_sql_query(
                        sql=f"SELECT * FROM {DB_DATA_TABLE_HYDROGRAPH}",
                        con=ENGINE_DATA
                    )
                    
                    indexes = data_exist[ (data_exist['MAHDOUDE'] == study_area) & (data_exist['AQUIFER'] == aquifer) ].index
                
                    data_exist.drop(indexes, inplace=True)
                    
                    frames = [data_exist, df]
                    
                    data = pd.concat(frames)
                    
                    data = data.sort_values(
                        by=["MAHDOUDE", "AQUIFER", "DATE_GREGORIAN"]
                    ).reset_index(drop=True)
                    
                    data.to_sql(
                        name=DB_DATA_TABLE_HYDROGRAPH,
                        con=ENGINE_DATA,
                        if_exists='replace',
                        index=False
                    )
                    
                    notify = dmc.Notification(
                        id ="notify",
                        title = "خبر",
                        message = ["هیدروگراف با موفقت ذخیره گردید!"],
                        color = 'green',
                        action = "show"
                    )
                    
                    result = [
                        0,
                        notify,
                    ]
                    
                    return result
                
                else:
                    
                    df.to_sql(
                        name=DB_DATA_TABLE_HYDROGRAPH,
                        con=ENGINE_DATA,
                        if_exists='replace',
                        index=False
                    )
                
                    notify = dmc.Notification(
                        id ="notify",
                        title = "خبر",
                        message = ["هیدروگراف با موفقت ذخیره گردید!"],
                        color = 'green',
                        action = "show"
                    )
                    
                    result = [
                        0,
                        notify,
                    ]
                    
                    return result
                    
            else:
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["ابتدا بر روی محاسبه هیدروگراف کلیک کنید!"],
                    color = 'red',
                    action = "show"
                )
                
                result = [
                    0,
                    notify,
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
                0,
                notify,
            ]
            
            return result
