import os
import json
import pandas as pd
import geopandas as gpd
import dash_bootstrap_components as dbc
from dash import dcc, dash_table, html, callback_context
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashLogger
import dash_mantine_components as dmc
import dash_datatables as ddt
from geoalchemy2 import Geometry, WKTElement
import plotly.graph_objects as go
import plotly.express as px
from . import *


def toolkits__groundWater__dataCleansing__dataEntry__callbacks(app):
    
    @app.callback(
        Output("download_xlsx", "data"),
        Input("btn_xlsx", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_template_file(
        n
    ):
        return dcc.send_file(
            "./Assets/Files/HydrographDataTemplate.xlsx"
    )
    
    @app.callback(
        Output("download_mashhad", "data"),
        Input("btn_mashhad", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_mashhad_file(
        n
    ):
        return dcc.send_file(
            "./Assets/Files/KhorasanRazavi.zip"
    )
    
    @app.callback(
        Output("CONTENT", "children"),
        Output('GEOINFO_TABLE_BUTTON', 'n_clicks'),
        Output('RAW_DATA_TABLE_BUTTON', 'n_clicks'),
        Output('WELL_MAP_BUTTON', 'n_clicks'),
        Output('STUDY_AREA_MAP_BUTTON', 'n_clicks'),
        Output("ALERTS", "children"),
        Input('GEOINFO_TABLE_BUTTON', 'n_clicks'),
        Input('RAW_DATA_TABLE_BUTTON', 'n_clicks'),
        Input('WELL_MAP_BUTTON', 'n_clicks'),
        Input('AQUIFER_MAP_BUTTON', 'n_clicks'),
        Input('STUDY_AREA_MAP_BUTTON', 'n_clicks'),
    )
    def show_content(
        n1, n2, n3, n4, n5
    ):
        ctx = callback_context
        
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if button_id == "GEOINFO_TABLE_BUTTON":
            
            try:
                df = pd.read_sql_query(
                    sql=f"SELECT * FROM geoinfo",
                    con=ENGINE_DATA
                )
                
                notify = dmc.Notification(
                    id="notify",
                    title = "خبر",
                    message = ["جدول مشخصات با موفقیت نمایش داده شد."],
                    color='green',
                    action = "show",
                )
                
                title = "جدول مشخصات"
                
                content = dash_table.DataTable(
                    columns=[
                        {"name": i, "id": i} for i in df.columns
                    ],
                    data=df.to_dict('records'),
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    sort_by=[
                        {"column_id": "MAHDOUDE", "direction": "asc"},
                        {"column_id": "AQUIFER", "direction": "asc"},
                        {"column_id": "LOCATION", "direction": "asc"},
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
            
            except:
                
                notify = dmc.Notification(
                    id="notify",
                    title = "خطا",
                    message = ["داده‌ای برای نمایش موجود نمی‌باشد!!!"],
                    color='red',
                    action = "show",
                )
                
                title = ""
                
                content = ""
            
            return [
                    [
                        html.H3(
                            className="pt-3",
                            children=title
                        ),
                        content,
                    ],
                    0,
                    0,
                    0,
                    0,
                    notify
                ]
        
        elif button_id == "RAW_DATA_TABLE_BUTTON":
            
            try:
                df = pd.read_sql_query(
                    sql=f"SELECT * FROM raw_data",
                    con=ENGINE_DATA
                )
                
                notify = dmc.Notification(
                    id="notify",
                    title = "خبر",
                    message = ["جدول داده‌ها با موفقیت نمایش داده شد."],
                    color='green',
                    action = "show",
                )
                
                title = "جدول داده‌ها"
                
                content = dash_table.DataTable(
                    columns=[
                        {"name": i, "id": i} for i in df.columns
                    ],
                    data=df.to_dict('records'),
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    sort_by=[
                        {"column_id": "MAHDOUDE", "direction": "asc"},
                        {"column_id": "AQUIFER", "direction": "asc"},
                        {"column_id": "LOCATION", "direction": "asc"},
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
            
            except:                
                notify = dmc.Notification(
                    id="notify",
                    title = "خطا",
                    message = ["داده‌ای برای نمایش موجود نمی‌باشد!!!"],
                    color='red',
                    action = "show",
                )                
                title = ""
                
                content = ""
            
            return [
                    [
                        html.H3(
                            className="pt-3",
                            children=title
                        ),
                        content,
                    ],
                    0,
                    0,
                    0,
                    0,
                    notify
                ]
            
        elif button_id == "STUDY_AREA_MAP_BUTTON":
            
            try:
                
                df = gpd.GeoDataFrame.from_postgis(
                    sql=f"SELECT * FROM {DB_LAYERS_TABLE_MAHDOUDE}",
                    con=ENGINE_LAYERS,
                    geom_col="geometry"
                )
                
                df_json = json.loads(df.to_json())

                for feature in df_json["features"]:
                    feature['id'] = feature['properties']['MAHDOUDE']
                
                fig = px.choropleth_mapbox(
                    data_frame=df,
                    geojson=df_json,
                    locations="MAHDOUDE",
                    hover_name="MAHDOUDE",
                    hover_data={"MAHDOUDE": False},
                    opacity=0.4,
                )           
                
                fig.update_layout(
                    mapbox = {
                        'style': "stamen-terrain",
                        'zoom': 6,
                        'center': {
                            'lat': df.geometry.centroid.y.mean(),
                            'lon': df.geometry.centroid.x.mean(),
                        },
                    },
                    showlegend = False,
                    hovermode='closest',
                    margin = {'l':0, 'r':0, 'b':0, 't':0}
                )
                
                notify = dmc.Notification(
                    id="notify",
                    title = "خبر",
                    message = ["نقشه با موفقیت نمایش داده شد."],
                    color='green',
                    action = "show",
                )
                
                title = "نقشه محدوده‌های مطالعاتی پایگاه داده"
                
                content = dcc.Graph(
                    className="border border-secondary",
                    style={
                        "height": "75vh",
                    },
                    figure=fig
                )
            
            except:                
                notify = dmc.Notification(
                    id="notify",
                    title = "خطا",
                    message = ["داده‌ای برای نمایش موجود نمی‌باشد!!!"],
                    color='red',
                    action = "show",
                )                
                title = ""
                
                content = ""
            
            return [
                    [
                        html.H3(
                            className="pt-3",
                            children=title
                        ),
                        content,
                    ],
                    0,
                    0,
                    0,
                    0,
                    notify
                ]
            
        elif button_id == "AQUIFER_MAP_BUTTON":
            
            try:
                
                df = gpd.GeoDataFrame.from_postgis(
                    sql=f"SELECT * FROM {DB_LAYERS_TABLE_AQUIFER}",
                    con=ENGINE_LAYERS,
                    geom_col="geometry"
                )
                
                df_json = json.loads(df.to_json())

                for feature in df_json["features"]:
                    feature['id'] = feature['properties']['AQUIFER']
                
                fig = px.choropleth_mapbox(
                    data_frame=df,
                    geojson=df_json,
                    locations="AQUIFER",
                    hover_name="AQUIFER",
                    hover_data={"MAHDOUDE": True, "AQUIFER": False},
                    opacity=0.4,
                    labels={'MAHDOUDE':'محدوده مطالعاتی', 'AQUIFER':'آبخوان'}
                )           
                
                fig.update_layout(
                    mapbox = {
                        'style': "stamen-terrain",
                        'zoom': 6,
                        'center': {
                            'lat': df.geometry.centroid.y.mean(),
                            'lon': df.geometry.centroid.x.mean(),
                        },
                    },
                    showlegend = False,
                    hovermode='closest',
                    margin = {'l':0, 'r':0, 'b':0, 't':0}
                )
                
                notify = dmc.Notification(
                    id="notify",
                    title = "خبر",
                    message = ["نقشه با موفقیت نمایش داده شد."],
                    color='green',
                    action = "show",
                )
                
                title = "نقشه آبخوان‌های پایگاه داده"
                
                content = dcc.Graph(
                    className="border border-secondary",
                    style={
                        "height": "75vh",
                    },
                    figure=fig
                )
            
            except:                
                notify = dmc.Notification(
                    id="notify",
                    title = "خطا",
                    message = ["داده‌ای برای نمایش موجود نمی‌باشد!!!"],
                    color='red',
                    action = "show",
                )                
                title = ""
                
                content = ""
            
            return [
                    [
                        html.H3(
                            className="pt-3",
                            children=title
                        ),
                        content,
                    ],
                    0,
                    0,
                    0,
                    0,
                    notify
                ]
            
        elif button_id == "WELL_MAP_BUTTON":
            
            try:
                
                df = gpd.GeoDataFrame.from_postgis(
                    sql=f"SELECT * FROM {DB_LAYERS_TABLE_WELL}",
                    con=ENGINE_LAYERS,
                    geom_col="geometry"
                )
                
                df_json = json.loads(df.to_json())

                for feature in df_json["features"]:
                    feature['id'] = feature['properties']['LOCATION']
                
                fig_data = go.Scattermapbox(
                    lat=df.Y,
                    lon=df.X,
                    mode='markers',
                    marker=go.scattermapbox.Marker(size=8),
                    text=[df['LOCATION'][i] + '<br>' + df['AQUIFER'][i] + '<br>' + df['MAHDOUDE'][i] for i in range(df.shape[0])],
                    hoverinfo='text',
                    hovertemplate='<span style="color:white;">%{text}</span><extra></extra>'
                )
                
                fig_layout = {
                    "margin": {'l':0, 'r':0, 'b':0, 't':0},
                    "mapbox": {
                        'style': "stamen-terrain",
                        'zoom': 6,
                        'center': {
                            'lat': df.Y.mean(),
                            'lon': df.X.mean(),
                        }
                    },
                    "showlegend": False,
                    "hovermode": 'closest'
                }
                
                fig = go.Figure(data=fig_data, layout=fig_layout)

                notify = dmc.Notification(
                    id="notify",
                    title = "خبر",
                    message = ["نقشه با موفقیت نمایش داده شد."],
                    color='green',
                    action = "show",
                )
                
                title = "نقشه چاه‌های مشاهده‌ای پایگاه داده"
                
                content = dcc.Graph(
                    className="border border-secondary",
                    style={
                        "height": "75vh",
                    },
                    figure=fig
                )
            
            except:
                
                notify = dmc.Notification(
                    id="notify",
                    title = "خطا",
                    message = ["داده‌ای برای نمایش موجود نمی‌باشد!!!"],
                    color='red',
                    action = "show",
                )                
                title = ""
                
                content = ""
            
            return [
                    [
                        html.H3(
                            className="pt-3",
                            children=title
                        ),
                        content,
                    ],
                    0,
                    0,
                    0,
                    0,
                    notify
                ]
        
        else:
            
            notify = dmc.Notification(
                id="notify",
                title = "",
                message = [""],
                color='red',
                action = "hide",
            )
                
            title = ""
            
            content = ""
            
            return [
                    [
                        html.H3(
                            className="pt-3",
                            children=title
                        ),
                        content,
                    ],
                    0,
                    0,
                    0,
                    0,
                    notify
                ]

    
    @app.callback(
        Output("ALERTS", "children"),
        Input('INTERVAL', 'n_intervals'),
    )
    def check_template_file(
        n
    ):
            list_files = []
            for x in os.listdir("./Assets/Files/"):
                if x.endswith(".xlsx") or x.endswith(".xls"):
                    list_files.append(x)
            
            if "HydrographDataTemplate.xlsx" not in list_files:
                notify = dmc.Notification(
                        id="notify",
                        title = "خطا",
                        message = ["فایل نمونه ورودی یافت نشد!"],
                        color='red',
                        action = "show",
                    )
            
                return notify

    
    @app.callback(
        Output("BUTTON-SHAPEFILES", "n_clicks"),
        Output("SELECT_SHAPEFILE_NAME", "children"),
        Output("SELECT_SHAPEFILE_NAME", "className"),
        Output("ALERTS", "children"),
        Input("BUTTON-SHAPEFILES", "n_clicks"),
        Input('SELECT_SHAPEFILE', 'contents'),        
        State('SELECT_SHAPEFILE', 'contents'),
        State('SELECT_SHAPEFILE', 'filename'),
        State('SHAPEFILE_TYPE', 'value'),
        State('GEODATABASE_MODIFY', 'value'),       
    )
    def upload_shapefiles(
        button_n_clicks,
        file_contents,
        file_contents_state,
        file_filename_state,        
        file_type_value_state,
        geodatabase_modify_value_state,
    ):
        if (button_n_clicks != 0 and file_contents is None):
            
            notify = dmc.Notification(
                id="notify",
                title = "هشدار",
                message = ["فایل فشرده‌ای انتخاب نشده است."],
                color='orange',
                action = "show",
            )
            
            result = [
                0,
                "فایلی انتخاب نشده است!",
                'text-center pt-2 text-danger',
                notify
            ]
            
            return result
        
        elif (button_n_clicks == 0 and file_contents is not None):
            
            notify = dmc.Notification(
                id="notify",
                title = "خبر",
                message = [f"فایل {file_filename_state} با موفقیت بارگذاری شد."],
                color="green",
                action = "show",
            )
            
            result = [
                0,
                f"{file_filename_state[0:12]}...{file_filename_state[-8:]}" if len(file_filename_state) > 20 else file_filename_state,
                'text-center pt-2 text-success',
                notify
            ]
            
            return result
        
        elif (button_n_clicks != 0 and file_contents is not None):
                
            notify = dmc.Notification(
                id="notify",
                title = "خبر",
                message = ["پایگاه داده با موفقیت ایجاد شد."],
                color="green",
                action = "show",
            )
            
            tmp = read_shapefile_from_zip_file(
                contents=file_contents,
                filename=file_filename_state,
                path_uploaded_files=PATH_UPLOADED_FILES,
                srid=4326,
            )        
            
            template = pd.ExcelFile(PATH_THEMPLATE_FILE)
                
            if file_type_value_state == "well":
                
                columns_template = pd.read_excel(template, sheet_name='Well').columns
                
                if set(tmp.columns) != set(columns_template):
                    
                    notify = dmc.Notification(
                        id="notify",
                        title = "خطا",
                        message = ["ستون‌های جدول شیپ فایل انتخابی با ستون‌های جدول نمونه برابر نیستند."],
                        color='red',
                        action = "show",
                    )
                    
                    result = [
                        0,
                        "فایلی انتخاب نشده است!",
                        'text-center pt-2 text-danger',
                        notify
                    ]
                    
                    return result
                
                else:
                    
                    tmp = tmp[columns_template]
                    fix_columns=["MAHDOUDE", "AQUIFER", "LOCATION"]
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.rstrip())
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.lstrip())
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.replace('ي','ی'))
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.replace('ئ','ی'))
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.replace('ك', 'ک'))
                    
                    tmp = tmp.drop_duplicates(subset=tmp.columns.difference(['ID'])).sort_values(
                        by=["MAHDOUDE", "AQUIFER", "LOCATION"]
                    ).reset_index(drop=True)                 
                    
                    check_replace_append(
                        data=tmp,
                        db=POSTGRES_DB_LAYERS,
                        table=DB_LAYERS_TABLE_WELL,
                        engine=ENGINE_LAYERS,
                        if_exists=geodatabase_modify_value_state,
                        geometry_type="POINT",
                        srid=4326,
                        geom_col="geometry",
                        sort_columns=["MAHDOUDE", "AQUIFER", "LOCATION"],
                    )
                    
                    notify = dmc.Notification(
                        id="notify",
                        title = "خبر",
                        message = ["شیپ فایل با موفقیت به پایگاه داده اضافه شد."],
                        color='green',
                        action = "show",
                    )
                        
                    result = [
                        0,
                        "فایلی انتخاب نشده است!",
                        'text-center pt-2 text-danger',
                        notify
                    ]
                        
                    return result
                
            elif file_type_value_state == "aquifer":
                
                columns_template = pd.read_excel(template, sheet_name='Aquifer').columns
                
                if set(tmp.columns) != set(columns_template):
                    
                    notify = dmc.Notification(
                        id="notify",
                        title = "خطا",
                        message = ["ستون‌های جدول شیپ فایل انتخابی با ستون‌های جدول نمونه برابر نیستند."],
                        color='red',
                        action = "show",
                    )
                    
                    result = [
                        0,
                        "فایلی انتخاب نشده است!",
                        'text-center pt-2 text-danger',
                        notify
                    ]
                    
                    return result
                
                else:
                    
                    tmp = tmp[columns_template]
                    fix_columns=["MAHDOUDE", "AQUIFER"]
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.rstrip())
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.lstrip())
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.replace('ي','ی'))
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.replace('ئ','ی'))
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.replace('ك', 'ک'))
                    
                    tmp = tmp.drop_duplicates().sort_values(
                        by=["MAHDOUDE", "AQUIFER"]
                    ).reset_index(drop=True)                   
                    
                    check_replace_append(
                        data=tmp,
                        db=POSTGRES_DB_LAYERS,
                        table=DB_LAYERS_TABLE_AQUIFER,
                        engine=ENGINE_LAYERS,
                        if_exists=geodatabase_modify_value_state,
                        geometry_type="MULTIPOLYGON",
                        srid=4326,
                        geom_col="geometry",
                        sort_columns=["MAHDOUDE", "AQUIFER"],
                    )
                    
                    notify = dmc.Notification(
                        id="notify",
                        title = "خبر",
                        message = ["شیپ فایل با موفقیت به پایگاه داده اضافه شد."],
                        color='green',
                        action = "show",
                    )
                        
                    result = [
                        0,
                        "فایلی انتخاب نشده است!",
                        'text-center pt-2 text-danger',
                        notify
                    ]
                        
                    return result
            elif file_type_value_state == "mahdoude":
                
                columns_template = pd.read_excel(template, sheet_name='Mahdoude').columns
                
                if set(tmp.columns) != set(columns_template):
                    
                    notify = dmc.Notification(
                        id="notify",
                        title = "خطا",
                        message = ["ستون‌های جدول شیپ فایل انتخابی با ستون‌های جدول نمونه برابر نیستند."],
                        color='red',
                        action = "show",
                    )
                    
                    result = [
                        0,
                        "فایلی انتخاب نشده است!",
                        'text-center pt-2 text-danger',
                        notify
                    ]
                    
                    return result
                
                else:
                    
                    tmp = tmp[columns_template]
                    fix_columns=["MAHDOUDE"]
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.rstrip())
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.lstrip())
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.replace('ي','ی'))
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.replace('ئ','ی'))
                    tmp[fix_columns] = tmp[fix_columns].apply(lambda x: x.str.replace('ك', 'ک'))
                    
                    tmp = tmp.drop_duplicates().sort_values(
                        by=["MAHDOUDE"]
                    ).reset_index(drop=True)                   
                    
                    check_replace_append(
                        data=tmp,
                        db=POSTGRES_DB_LAYERS,
                        table=DB_LAYERS_TABLE_MAHDOUDE,
                        engine=ENGINE_LAYERS,
                        if_exists=geodatabase_modify_value_state,
                        geometry_type="MULTIPOLYGON",
                        srid=4326,
                        geom_col="geometry",
                        sort_columns=["MAHDOUDE"],
                    )
                    
                    notify = dmc.Notification(
                        id="notify",
                        title = "خبر",
                        message = ["شیپ فایل با موفقیت به پایگاه داده اضافه شد."],
                        color='green',
                        action = "show",
                    )
                        
                    result = [
                        0,
                        "فایلی انتخاب نشده است!",
                        'text-center pt-2 text-danger',
                        notify
                    ]
                        
                    return result
            else:
                
                notify = dmc.Notification(
                    id="notify",
                    title = "",
                    message = [""],
                    color='orange',
                    action = "hide",
                )
                
                result = [
                    0,
                    "فایلی انتخاب نشده است!",
                    'text-center pt-2 text-danger',
                    notify
                ]
                
                return result
        
        else:
            
            notify = dmc.Notification(
                id="notify",
                title = "",
                message = [""],
                color='orange',
                action = "hide",
            )
            
            result = [
                0,
                "فایلی انتخاب نشده است!",
                'text-center pt-2 text-danger',
                notify
            ]
            
            return result

    
    
    
    
    @app.callback(
        Output("BUTTON-DATA", "n_clicks"),
        Output("SELECT_FILE_NAME", "children"),
        Output("SELECT_FILE_NAME", "style"),
        Output('SELECT_FILE', 'contents'),
        Output('SELECT_GEOINFO_WORKSHEET', 'options'),
        Output('SELECT_DATA_WORKSHEET', 'options'),
        Output('STORAGE', 'data'),
        Output("ALERTS", "children"),
        
        Input("BUTTON-DATA", "n_clicks"),
        Input('SELECT_FILE', 'contents'),        
        State('SELECT_FILE', 'contents'),
        State('SELECT_FILE', 'filename'),        
        State('SELECT_GEOINFO_WORKSHEET', 'value'),
        State('SELECT_GEOINFO_WORKSHEET', 'options'),
        State('SELECT_DATA_WORKSHEET', 'value'),      
        State('SELECT_DATA_WORKSHEET', 'options'),
        State('DATABASE_MODIFY', 'value'),
        State('STORAGE', 'data'),
    )
    def dataEntry__callbacks(
        button_n_clicks,
        file_contents,
        file_contents_state,
        file_filename_state,
        geoInfo_worksheet_value_state,
        geoInfo_worksheet_options_state,
        data_worksheet_value_state,
        data_worksheet_options_state,
        database_modify_value_state,
        storage_state,
    ):
        
        if (button_n_clicks != 0 and file_contents is None):
            
            notify = dmc.Notification(
                id="notify",
                title = "هشدار",
                message = ["فایل صفحه گسترده‌ای انتخاب نشده است."],
                color='orange',
                action = "show",
            )
            
            result = [
                0,
                "فایلی انتخاب نشده است!",
                {'direction': 'rtl', 'color': 'red', 'text-align': 'center'},
                None,
                [],
                [],
                None,
                notify
            ]
            
            return result
        
        elif (button_n_clicks == 0 and file_contents is not None):
            
            data, worksheet_name = read_data_from_spreadsheet(
                contents=file_contents,
                filename=file_filename_state
            )
            
            if worksheet_name is None:
                
                notify = dmc.Notification(
                    id="notify",
                    title = "هشدار",
                    message = ["تعداد کاربرگ‌های فایل ورودی باید حداقل دو عدد باشند."],
                    color='orange',
                    action = "show",
                )
                
                result = [
                    0,
                    "فایلی انتخاب نشده است!",
                    {'direction': 'rtl', 'color': 'red', 'text-align': 'center'},
                    None,
                    [],
                    [],
                    None,
                    notify
                ]
                
                return result
            
            else:
                
                notify = dmc.Notification(
                    id="notify",
                    title = "خبر",
                    message = [f"فایل {file_filename_state} با موفقیت بارگذاری شد."],
                    color="green",
                    action = "show",
                )
                
                result = [
                    0,
                    f"{file_filename_state[0:12]}...{file_filename_state[-8:]}" if len(file_filename_state) > 20 else file_filename_state,
                    {'direction': 'rtl', 'color': 'green', 'text-align': 'left'},
                    file_contents_state,
                    [{'label': wn, 'value': wn} for wn in worksheet_name],
                    [{'label': wn, 'value': wn} for wn in worksheet_name],
                    data,
                    notify
                ]
            
            return result
        
        elif (button_n_clicks != 0 and file_contents is not None):

            template_xlsx = pd.ExcelFile(PATH_THEMPLATE_FILE)
            geoinfo_columns_template_xlsx = pd.read_excel(template_xlsx, sheet_name='GeoInfo').columns
            data_columns_template_xlsx = pd.read_excel(template_xlsx, sheet_name='Data').columns

            
            if (geoInfo_worksheet_value_state is None) | (data_worksheet_value_state is None):
                
                notify = dmc.Notification(
                    id="notify",
                    title = "هشدار",
                    message = ["کاربرگ مشخصات یا کاربرگ داده‌ها انتخاب نشده است!"],
                    color="orange",
                    action = "show",
                )
                
                result = [
                    1,
                    f"{file_filename_state[0:12]}...{file_filename_state[-8:]}" if len(file_filename_state) > 20 else file_filename_state,
                    {'direction': 'rtl', 'color': 'green', 'text-align': 'left'},
                    file_contents_state,
                    geoInfo_worksheet_options_state,
                    data_worksheet_options_state,
                    storage_state,
                    notify
                ]
                
                return result
            
            elif geoInfo_worksheet_value_state == data_worksheet_value_state:
                
                notify = dmc.Notification(
                    id="notify",
                    title = "هشدار",
                    message = ["کاربرگ مشخصات و کاربرگ داده‌ها نمی‌توانند یکسان باشند!"],
                    color="orange",
                    action = "show",
                )
                
                result = [
                    1,
                    f"{file_filename_state[0:12]}...{file_filename_state[-8:]}" if len(file_filename_state) > 20 else file_filename_state,
                    {'direction': 'rtl', 'color': 'green', 'text-align': 'left'},
                    file_contents_state,
                    geoInfo_worksheet_options_state,
                    data_worksheet_options_state,
                    storage_state,
                    notify
                ]
                                
                return result
            
            elif set(storage_state[geoInfo_worksheet_value_state].keys()) != set(geoinfo_columns_template_xlsx):
                
                notify = dmc.Notification(
                    id="notify",
                    title = "هشدار",
                    message = ["سر ستون‌های «کاربرگ مشخصات» با فایل نمونه همخوانی ندارند!"],
                    color="orange",
                    action = "show",
                )
                
                result = [
                    0,
                    "فایلی انتخاب نشده است!",
                    {'direction': 'rtl', 'color': 'red', 'text-align': 'center'},
                    None,
                    [],
                    [],
                    None,
                    notify      
                ]
                
                return result
            
            elif set(storage_state[data_worksheet_value_state].keys()) != set(data_columns_template_xlsx):
                
                notify = dmc.Notification(
                    id="notify",
                    title = "هشدار",
                    message = ["سر ستون‌های «کاربرگ داده‌ها» با فایل نمونه همخوانی ندارند!"],
                    color="orange",
                    action = "show",
                )
                
                result = [
                    0,
                    "فایلی انتخاب نشده است!",
                    {'direction': 'rtl', 'color': 'red', 'text-align': 'center'},
                    None,
                    [],
                    [],
                    None,
                    notify      
                ]
                
                return result
            
            else:
                
                notify = dmc.Notification(
                    id="notify",
                    title = "خبر",
                    message = ["پایگاه داده با موفقیت ایجاد شد."],
                    color="green",
                    action = "show",
                )
                
                delete_table()
                
                create_geoinfo_data_table(
                    geoinfo_data = pd.DataFrame.from_dict(storage_state[geoInfo_worksheet_value_state]),
                    engine = ENGINE_DATA,
                    table_name = DB_DATA_TABLE_GEOINFO,
                    geoinfo_data_column = geoinfo_columns_template_xlsx,
                    if_exists = database_modify_value_state
                )
                
                create_raw_data_table(
                    raw_data = pd.DataFrame.from_dict(storage_state[data_worksheet_value_state]),
                    engine = ENGINE_DATA,
                    table_name = DB_DATA_TABLE_RAWDATA,
                    raw_data_column = data_columns_template_xlsx,
                    if_exists = database_modify_value_state,
                )
                
                clean_geoinfo_raw_data_table(
                    engine = ENGINE_DATA,
                    table_name_geoinfo = DB_DATA_TABLE_GEOINFO,
                    table_name_raw_data = DB_DATA_TABLE_RAWDATA,
                )
                
                create_update_modified_data_table(
                    engine = ENGINE_DATA,
                    table_name_raw_data = DB_DATA_TABLE_RAWDATA,
                    table_name_modified_data = DB_DATA_TABLE_MODIFIEDDATA,
                    table_name_raw_data_deleted = DB_DATA_TABLE_RAW_DATA_DELETED,
                    table_name_raw_data_modified = DB_DATA_TABLE_RAW_DATA_MODIFIED,
                    sort_columns = SORT_COLUMNS,
                    if_exists = database_modify_value_state
                )
                
                result = [
                    0,
                    "فایلی انتخاب نشده است!",
                    {'direction': 'rtl', 'color': 'red', 'text-align': 'center'},
                    None,
                    [],
                    [],
                    None,
                    notify      
                ]
                
                return result
        
        else:
            
            notify = dmc.Notification(
                id="notify",
                title = "",
                message = [""],
                color='orange',
                action = "hide",
            )
            
            result = [
                0,
                "فایلی انتخاب نشده است!",
                {'direction': 'rtl', 'color': 'red', 'text-align': 'center'},
                None,
                [],
                [],
                None,
                notify      
            ]
            
            return result