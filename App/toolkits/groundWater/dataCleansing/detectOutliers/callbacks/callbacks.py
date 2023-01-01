import os
import json
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import pandas as pd
import numpy as np
import geopandas as gpd
from dash import no_update, html, dash_table, dcc
from dash.dependencies import Output, Input, State
import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px
from . import *



def toolkits__groundWater__dataCleansing__detectOutliers__callbacks(app):
    
    @app.callback(
        Output('MAP', 'figure'),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
    )
    def map(
        study_area, aquifer, well
    ):
        if (study_area is not None and len(study_area) != 0) & (aquifer is not None and len(aquifer) != 0) & (well is not None and len(well) != 0) :

            
            try:
                # MAHDOUDE
                if len(study_area) == 1:
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_MAHDOUDE} WHERE \"MAHDOUDE\" = '{study_area[0]}'"
                else:
                    sql = f'SELECT * FROM {DB_LAYERS_TABLE_MAHDOUDE} WHERE "MAHDOUDE" IN {*study_area,}'
                
                df_study_area = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=ENGINE_LAYERS,
                    geom_col="geometry"
                )
                
                df_study_area_json = json.loads(df_study_area.to_json())
                
                for feature in df_study_area_json["features"]:
                    feature['id'] = feature['properties']['MAHDOUDE']
                
                # AQUIFER            
                if (len(study_area) == 1) and (len(aquifer) == 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}'"
                elif (len(study_area) == 1) and (len(aquifer) != 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,}"
                elif (len(study_area) != 1) and (len(aquifer) == 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}'"
                else:
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" IN {*aquifer,}"

                df_aquifer = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=ENGINE_LAYERS,
                    geom_col="geometry"
                )
                
                df_aquifer_json = json.loads(df_aquifer.to_json())
                
                for feature in df_aquifer_json["features"]:
                    feature['id'] = feature['properties']['AQUIFER']
                
                # WELL
                if (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) != 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" IN {*well,}"
                elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) != 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                elif (len(study_area) != 1) and (len(aquifer) != 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                elif (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) != 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                else:
                    sql = f'SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE ("MAHDOUDE" IN {*study_area,} AND "AQUIFER" IN {*aquifer,} AND "LOCATION" IN {*well,})'
                
                df_well = gpd.GeoDataFrame.from_postgis(
                    sql=sql,
                    con=ENGINE_LAYERS,
                    geom_col="geometry"
                )
                
                # ALL WELL
                if len(study_area) == 1 and len(aquifer) == 1:
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}'"
                elif len(study_area) != 1 and len(aquifer) == 1:
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}'"
                elif len(study_area) == 1 and len(aquifer) != 1:
                    sql = f"SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,}"
                else:
                    sql = f'SELECT * FROM {DB_LAYERS_TABLE_WELL} WHERE ("MAHDOUDE" IN {*study_area,} AND "AQUIFER" IN {*aquifer,})'
                
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



    @app.callback(
        Output('AQUIFER_SELECT', 'options'),
        Input('STUDY_AREA_SELECT', 'value'),
    )
    def aquifer_select(
        study_area_selected
    ):
        if study_area_selected is not None and len(study_area_selected) != 0:
            
            REDIS_DB.set('detectOutliers_studyArea', json.dumps(study_area_selected))
            
            df = pd.read_sql_query(
                sql=f'SELECT DISTINCT "MAHDOUDE", "AQUIFER" FROM geoinfo;',
                con=ENGINE_DATA
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
                
                REDIS_DB.set('detectOutliers_aquifer', json.dumps(aquifer_selected))
                
                df = pd.read_sql_query(
                    sql=f'SELECT DISTINCT "MAHDOUDE", "AQUIFER", "LOCATION" FROM geoinfo;',
                    con=ENGINE_DATA
                )
                df = df[df["MAHDOUDE"].isin(study_area_selected)]
                df = df[df["AQUIFER"].isin(aquifer_selected)]
                return [{'label': i, 'value': i} for i in sorted(df.LOCATION.values)]
            else:
                return [{}]
        else:
            return [{}]
    
    
    
    @app.callback(
        Output('STUDY_AREA_SELECT', 'value'),
        Output('AQUIFER_SELECT', 'value'),
        Output('WELL_SELECT', 'value'),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
    )
    def update_dropdown_list(study_area, aquifer, well):
        
        try:

            if (study_area is not None and len(study_area) != 0) and\
                    (aquifer is None or len(aquifer) == 0) and\
                        (well is not None and len(well) != 0):
                            
                            result = [
                                no_update,
                                [],
                                []
                            ]
                            return result
                        
                        
            elif (study_area is None or len(study_area) == 0) and\
                    (aquifer is not None and len(aquifer) != 0) and\
                        (well is not None and len(well) != 0):
                            
                            result = [
                                [],
                                [],
                                []
                            ]
                            return result
            
            elif ((REDIS_DB.get('detectOutliers_studyArea') is not None) and (set(study_area) != set(json.loads(REDIS_DB.get('detectOutliers_studyArea').decode('utf-8'))))):
                        
                result = [
                    no_update,
                    [],
                    []
                ]
                return result
            elif ((REDIS_DB.get('detectOutliers_aquifer') is not None) and (set(aquifer) != set(json.loads(REDIS_DB.get('detectOutliers_aquifer').decode('utf-8'))))):
                
                result = [
                    no_update,
                    no_update,
                    []
                ]
                return result
                
                        
            else:
                
                result = [
                    no_update,
                    no_update,
                    no_update
                ]
                return result
        except:
            
                result = [
                    no_update,
                    no_update,
                    no_update
                ]
                return result
    
    
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
            
            if storage_state[DB_DATA_TABLE_MODIFIEDDATA]:
                
                df_selected_modify = pd.DataFrame(data_table_state)
                
                if len(df_selected_modify) != 0:
                
                    try:
                        df_selected_modify["DESCRIPTION"] = df_selected_modify["DESCRIPTION"] + "تاریخ اصلاح شده است."
                    except:
                        pass
                                
                df = pd.read_sql_query(
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA}",
                    con = ENGINE_DATA
                ).reset_index().rename(columns = {'index':'idx'})
                
                df = df.drop(storage_state["index_wrong_date"])

                df = pd.concat([df, df_selected_modify]).reset_index(drop=True).drop(columns=['idx'])
                
                df["DATE_GREGORIAN"] = df["DATE_GREGORIAN"].apply(pd.to_datetime)
                
                df['WATER_TABLE'] = df['WATER_TABLE'].astype('float64')
                
                df.to_sql(
                    name=DB_DATA_TABLE_MODIFIEDDATA,
                    con=ENGINE_DATA,
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
        Input('SELECT_DATE_TYPE', 'value'),
        State('STORAGE', 'data'),
    )
    def show_wrong_date(
        n_btn_show_wrong_date, date_type, storage_state
    ):
        if (n_btn_show_wrong_date != 0):
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
                
            if DB_DATA_TABLE_MODIFIEDDATA not in table_name_list_exist:
                
                storage_state[DB_DATA_TABLE_MODIFIEDDATA] = False
                
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
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA}",
                    con = ENGINE_DATA
                ).reset_index().rename(columns = {'index':'idx'})
                
                storage_state[DB_DATA_TABLE_MODIFIEDDATA] = True
                                
                # if "zeros" in action_type:
                    
                #     df.drop(df[df.WATER_TABLE <= 0].index, inplace=True)
                    
                if date_type == "persian_ymd":
                    
                    cols = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
                    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
                    df[cols] = df[cols].astype(pd.Int64Dtype())
                    date_persian, date_gregorian = np.vectorize(check_persian_date_ymd)(df.YEAR_PERSIAN, df.MONTH_PERSIAN, df.DAY_PERSIAN)
                    df["DATE_PERSIAN"] = list(date_persian)
                    df["DATE_GREGORIAN"] = list(date_gregorian)
                    
                    index_wrong_date = df[df['DATE_GREGORIAN'].isnull()].index.tolist()
                    df_wrong_date = df[df['DATE_GREGORIAN'].isna()]
                    
                    df_duplicated = df[df.duplicated(subset=['MAHDOUDE', 'AQUIFER', 'LOCATION', 'YEAR_PERSIAN', 'MONTH_PERSIAN'], keep=False)]
                    df_duplicated_index = df[df.duplicated(subset=['MAHDOUDE', 'AQUIFER', 'LOCATION', 'YEAR_PERSIAN', 'MONTH_PERSIAN'], keep=False)].index
                    
                    index_wrong_date = list(index_wrong_date) + list(df_duplicated_index)
                    
                    df_wrong_date = pd.concat([df_wrong_date, df_duplicated]).sort_values(
                        by=['MAHDOUDE', 'AQUIFER', 'LOCATION', 'YEAR_PERSIAN', 'MONTH_PERSIAN']
                    ).reset_index(drop=True)
                    
                    
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
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA}",
                    con = ENGINE_DATA
                )
                
                if date_type == "persian_ymd":
                    
                    cols_p = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
                    cols_g = ['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']                       
                    df[cols_p] = df[cols_p].apply(pd.to_numeric, errors='coerce')
                    df[cols_p] = df[cols_p].astype(pd.Int64Dtype())
                    date_persian, date_gregorian = np.vectorize(check_persian_date_ymd)(df.YEAR_PERSIAN, df.MONTH_PERSIAN, df.DAY_PERSIAN)
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
                
                df = df.groupby(
                    by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                ).apply(
                    lambda x: fill_gap_date(
                        df=x
                    )
                ).reset_index(drop=True)
                
                df['DESCRIPTION'] = df['DESCRIPTION'].fillna("")
                
                df.to_sql(
                    name=DB_DATA_TABLE_MODIFIEDDATA,
                    con=ENGINE_DATA,
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
        Output("GRAPH", "figure"),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        Input('MEAN_METHOD', 'value'),
        Input('DERIVATIVE_METHOD', 'value'),
    )
    def show_graph(
        study_area, aquifer, well, mean, derivation
    ):
        if study_area is not None and len(study_area) != 0 and\
            aquifer is not None and len(aquifer) != 0 and\
                well is not None and len(well) != 0:
                
                    if (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) == 1):
                        sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                    elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) != 1):
                        sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" IN {*well,}"
                    elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) != 1):
                        sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                    elif (len(study_area) != 1) and (len(aquifer) != 1) and (len(well) == 1):
                        sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                    elif (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) != 1):
                        sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                    elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) == 1):
                        sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                    elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) == 1):
                        sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                    else:
                        sql = f'SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE ("MAHDOUDE" IN {*study_area,} AND "AQUIFER" IN {*aquifer,} AND "LOCATION" IN {*well,})'
                
                    df_m = pd.read_sql_query(
                        sql = sql,
                        con = ENGINE_DATA
                    )
                    
                    col_sort = ['MAHDOUDE', 'AQUIFER', 'LOCATION', 'DATE_GREGORIAN']                
                    df_modified = df_m.drop_duplicates().sort_values(by=col_sort).reset_index(drop=True).copy()
                    
                    if len(df_modified["WATER_TABLE"].dropna().to_list()) == 0:
                        return NO_MATCHING_GRAPH_FOUND
                        
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
                        
                        tmp = df[df["DESCRIPTION"].str.contains("تاریخ اصلاح شده است.")]
                        
                        fig.add_trace(
                            go.Scatter(
                                x=tmp['DATE_GREGORIAN'],
                                y=tmp['WATER_TABLE'],
                                mode='markers',
                                name=f'تاریخ اصلاح شده',
                                marker=dict(
                                    color='black',
                                    size=12,
                                ),
                            )
                        )                        
                        
                        tmp = df[df["DESCRIPTION"].str.contains("سطح ایستابی اصلاح شده است.")]
                        
                        fig.add_trace(
                            go.Scatter(
                                x=tmp['DATE_GREGORIAN'],
                                y=tmp['WATER_TABLE'],
                                mode='markers',
                                name=f'سطح ایستابی اصلاح شده',
                                marker=dict(
                                    color='red',
                                    size=8,
                                ),
                            )
                        )
                        
                        
                        tmp = df[df["WATER_TABLE"] == 0]
                        
                        fig.add_trace(
                            go.Scatter(
                                x=tmp['DATE_GREGORIAN'],
                                y=tmp['WATER_TABLE'],
                                mode='markers',
                                name=f'سطح ایستابی با مقدار صفر',
                                marker=dict(
                                    color='violet',
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
                    )

                    return fig
                    
                    # except:
                        
                    #     return NO_MATCHING_GRAPH_FOUND
        else:
            
            return NO_MATCHING_GRAPH_FOUND
    
    
    @app.callback(
        Output("DIV_TABLE", "children"),        
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
    )
    def show_table(
        study_area, aquifer, well
    ):
        if study_area is not None and len(study_area) != 0 and\
            aquifer is not None and len(aquifer) != 0 and\
                well is not None and len(well) != 0:
                    
                    try:
                
                        if (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) == 1):
                            sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                        elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) != 1):
                            sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" IN {*well,}"
                        elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) != 1):
                            sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                        elif (len(study_area) != 1) and (len(aquifer) != 1) and (len(well) == 1):
                            sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                        elif (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) != 1):
                            sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                        elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) == 1):
                            sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                        elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) == 1):
                            sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                        else:
                            sql = f'SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE ("MAHDOUDE" IN {*study_area,} AND "AQUIFER" IN {*aquifer,} AND "LOCATION" IN {*well,})'
                    
                        df_m = pd.read_sql_query(
                            sql = sql,
                            con = ENGINE_DATA
                        )
                        
                        df_m["DATE_GREGORIAN"] = df_m["DATE_GREGORIAN"].dt.strftime('%Y-%m-%d')
                        
                        if well is not None and len(well) == 1:
                            
                            table = dash_table.DataTable(
                                id="TABLE",
                                data=df_m.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in df_m.columns],
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
                            
                            return [
                                html.H3(
                                    className="pt-3",
                                    children=f"داده‌های سطح ایستابی چاه مشاهده‌ای {well[0]}"
                                ),
                                table,
                            ]
                            
                        else:
                            return []
                    
                    except:
                        return []
        else:
            return []
    
    
    
    @app.callback(
        Output("DIV_TABLE_SELECTED_DATA", "hidden"),
        Output("DIV_TABLE_SELECTED_DATA", "children"),
        Output('STORAGE', 'data'),
        Input("GRAPH", "selectedData"),
        Input('STUDY_AREA_SELECT', 'value'),
        Input('AQUIFER_SELECT', 'value'),
        Input('WELL_SELECT', 'value'),
        State('STORAGE', 'data'),
    )
    def show_table_selected_data(
        selectedData, study_area, aquifer, well, storage_state
    ):
        if well is not None and len(well) == 1:
            if selectedData is not None:
                if (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) != 1):
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" IN {*well,}"
                elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) != 1):
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                elif (len(study_area) != 1) and (len(aquifer) != 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                elif (len(study_area) == 1) and (len(aquifer) == 1) and (len(well) != 1):
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" IN {*well,}"
                elif (len(study_area) == 1) and (len(aquifer) != 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" = '{study_area[0]}' AND \"AQUIFER\" IN {*aquifer,} AND \"LOCATION\" = '{well[0]}'"
                elif (len(study_area) != 1) and (len(aquifer) == 1) and (len(well) == 1):
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE \"MAHDOUDE\" IN {*study_area,} AND \"AQUIFER\" = '{aquifer[0]}' AND \"LOCATION\" = '{well[0]}'"
                else:
                    sql = f'SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA} WHERE ("MAHDOUDE" IN {*study_area,} AND "AQUIFER" IN {*aquifer,} AND "LOCATION" IN {*well,})'
            
                df = pd.read_sql_query(
                    sql = sql,
                    con = ENGINE_DATA
                )
                
                if len(selectedData["points"]) != 0:
                    
                    point_selected = pd.DataFrame(selectedData["points"])
                    point_selected = point_selected[point_selected["curveNumber"] == 0]
                    df_selected = df[df["DATE_PERSIAN"].isin(point_selected["x"].tolist())]
                                        
                    df_table_database = pd.read_sql_query(
                        sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA}",
                        con = ENGINE_DATA
                    )
                    
                    ind = df_table_database.MAHDOUDE.isin(df_selected.MAHDOUDE) &\
                        df_table_database.AQUIFER.isin(df_selected.AQUIFER) &\
                            df_table_database.LOCATION.isin(df_selected.LOCATION) &\
                                df_table_database.DATE_PERSIAN.isin(df_selected.DATE_PERSIAN)
                                
                    ind = df_table_database[ind].index.tolist()
                    
                    storage_state["index_selected_data"] = ind
                    
                    df_selected["DATE_GREGORIAN"] = df_selected["DATE_GREGORIAN"].dt.strftime('%Y-%m-%d')
                    
                    table_selected_data = dash_table.DataTable(
                        id="TABLE_SELECTED_DATA",
                        columns=[{"name": i, "id": i, "editable": True if i == "WATER_TABLE" else False} for i in df_selected.columns],
                        data=df_selected.to_dict("records"),
                        editable=True,
                        row_deletable=True,
                        page_size=12,
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
                    
                    result = [
                        False,
                        [
                            html.H3(
                                className="pt-3",
                                children="جدول داده‌های انتخاب شده از نمودار"
                            ),
                            table_selected_data,
                        ],
                        storage_state
                    ]
                    return result
                else:
                    storage_state["index_selected_data"] = []
                    result = [
                        True,
                        None,
                        storage_state
                    ]
                    return result
            else:
                storage_state["index_selected_data"] = []
                result = [
                    True,
                    None,
                    storage_state
                ]
                return result
        else:
            storage_state["index_selected_data"] = []
            result = [
                True,
                None,
                storage_state
            ]
            return result
    

    
    @app.callback(
        Output("BUTTON_TABLE_GRAPH", "n_clicks"),
        Output("ALERTS", "children"),
        Output('STORAGE', 'data'),
        Input('WELL_SELECT', 'value'),
        Input("BUTTON_TABLE_GRAPH", "n_clicks"),
        State("TABLE_SELECTED_DATA", "data"),
        State('STORAGE', 'data'),
    )
    def modify_selected_data(
        well_selected, n_clicks, table_selected_data_state, storage_state
    ):
        if n_clicks != 0:
            
            if well_selected is not None and len(well_selected) == 1:
            
                if len(storage_state["index_selected_data"]) != 0:
                    
                    df = pd.read_sql_query(
                        sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA}",
                        con = ENGINE_DATA
                    )
                    
                    df_selected_data = pd.DataFrame(table_selected_data_state) 
                    
                    if df_selected_data.shape[0] != 0:
                        
                        study_area = df_selected_data["MAHDOUDE"].unique()[0]
                        aquifer = df_selected_data["AQUIFER"].unique()[0]
                        well = df_selected_data["LOCATION"].unique()[0]
                        
                        for i, row in df_selected_data.iterrows():
                            
                            date_persian = row["DATE_PERSIAN"]
                            
                            if df.loc[(df.MAHDOUDE == study_area) & (df.AQUIFER == aquifer) & (df.LOCATION == well) & (df.DATE_PERSIAN == date_persian)]["WATER_TABLE"].item() != df_selected_data.loc[(df_selected_data.MAHDOUDE == study_area) & (df_selected_data.AQUIFER == aquifer) & (df_selected_data.LOCATION == well) & (df_selected_data.DATE_PERSIAN == date_persian)]["WATER_TABLE"].item():
                                
                                df_selected_data.loc[i, "DESCRIPTION"] = df_selected_data.loc[i, "DESCRIPTION"] +  "سطح ایستابی اصلاح شده است."                    
                    
                    df = df.drop(storage_state["index_selected_data"])
                    
                    df = pd.concat([df, df_selected_data]).reset_index(drop=True)
                    
                    df['WATER_TABLE'] = df['WATER_TABLE'].astype('float64')
                    
                    df["DATE_GREGORIAN"] = df["DATE_GREGORIAN"].apply(pd.to_datetime)
                                        
                    if len(storage_state["index_selected_data"]) != 0:
                        
                        tmp = df.iloc[storage_state["index_selected_data"], :]                        
                        study_area = tmp["MAHDOUDE"].unique()[0]
                        aquifer = tmp["AQUIFER"].unique()[0]
                        well = tmp["LOCATION"].unique()[0] 
                                               
                        df_w = df.loc[(df.MAHDOUDE == study_area) & (df.AQUIFER == aquifer) & (df.LOCATION == well)]                        
                        df_w_index = df.loc[(df.MAHDOUDE == study_area) & (df.AQUIFER == aquifer) & (df.LOCATION == well)].index                        
                        df_w = fill_gap_date(df=df_w)                        
                        df_w['DESCRIPTION'] = df_w['DESCRIPTION'].fillna("")
                        df.drop(df_w_index , inplace=True)
                        df = pd.concat([df, df_w]).sort_values(
                            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
                        ).reset_index(drop=True)
                    
                    
                    
                    df.to_sql(
                        name=DB_DATA_TABLE_MODIFIEDDATA,
                        con=ENGINE_DATA,
                        if_exists='replace',
                        index=False
                    )
                    
                    storage_state["index_selected_data"] = []
                    
                    notify = dmc.Notification(
                        id ="notify",
                        title = "خبر",
                        message = ["پایگاه داده با موفقیت بروزرسانی شد."],
                        color = 'green',
                        action = "show",
                    )
                            
                    result = [
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
                        storage_state,
                        notify
                    ]
                    
                    return result
            
            else:
                
                notify = dmc.Notification(
                    id ="notify",
                    title = "خطا",
                    message = ["فقط یک چاه میتواند انتخاب شود!"],
                    color = 'red',
                    action = "show",
                )
                        
                result = [
                    0,
                    storage_state,
                    notify
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
                storage_state,
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
                
            if DB_DATA_TABLE_MODIFIEDDATA in table_name_list_exist:
            
                df = pd.read_sql_query(
                    sql = f"SELECT * FROM {DB_DATA_TABLE_MODIFIEDDATA}",
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

                return dcc.send_bytes(to_xlsx, "modified_data.xlsx")
            
            else:
                
                return no_update
        
        return no_update