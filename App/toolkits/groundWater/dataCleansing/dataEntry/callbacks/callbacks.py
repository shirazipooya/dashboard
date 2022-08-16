import os
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashLogger
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from . import *


def toolkits__groundWater__dataCleansing__dataEntry__callbacks(app):
    
    @app.callback(
        Output("TABLE", "children"),
        Output('GEOINFO_TABLE_BUTTON', 'n_clicks'),
        Output('RAW_DATA_TABLE_BUTTON', 'n_clicks'),
        Input('GEOINFO_TABLE_BUTTON', 'n_clicks'),
        Input('RAW_DATA_TABLE_BUTTON', 'n_clicks'),
    )
    def show_geoinfo_table(
        n1, n2
    ):
        if n1:
            
            df = pd.read_sql_query(
                sql=f"SELECT * FROM geoinfo",
                con=engine
            )
            
            return [
                dbc.Table.from_dataframe(
                    df,
                    striped=True,
                    bordered=True,
                    hover=True,
                    index=True
                ),
                0,
                0
            ]
        elif n2:
            
            df = pd.read_sql_query(
                sql=f"SELECT * FROM raw_data",
                con=engine
            )
            
            return [
                dbc.Table.from_dataframe(
                    df,
                    striped=True,
                    bordered=True,
                    hover=True,
                    index=True
                ),
                0,
                0
            ]
        else:
            return [
                PreventUpdate,
                0,
                0
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
        Output("BUTTON", "n_clicks"),
        Output("SELECT_FILE_NAME", "children"),
        Output("SELECT_FILE_NAME", "style"),
        Output('SELECT_FILE', 'contents'),
        Output('SELECT_GEOINFO_WORKSHEET', 'options'),
        Output('SELECT_DATA_WORKSHEET', 'options'),
        Output('STORAGE', 'data'),
        Output("ALERTS", "children"),
        
        Input("BUTTON", "n_clicks"),
        Input('SELECT_FILE', 'contents'),        
        State('SELECT_FILE', 'contents'),
        State('SELECT_FILE', 'filename'),        
        State('SELECT_GEOINFO_WORKSHEET', 'value'),
        State('SELECT_GEOINFO_WORKSHEET', 'options'),
        State('SELECT_DATA_WORKSHEET', 'value'),      
        State('SELECT_DATA_WORKSHEET', 'options'),
        State("SELECT_DATE_TYPE", "value"),
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
        date_type_value_state,
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
                
                create_geoinfo_data_table(
                    geoinfo_data = pd.DataFrame.from_dict(storage_state[geoInfo_worksheet_value_state]),
                    engin = engine,
                    table_name = "geoinfo",
                    geoinfo_data_column = geoinfo_columns_template_xlsx,
                    if_exists = database_modify_value_state
                )
                
                create_raw_data_table(
                    raw_data = pd.DataFrame.from_dict(storage_state[data_worksheet_value_state]),
                    engin = engine,
                    table_name = "raw_data",
                    raw_data_column = data_columns_template_xlsx,
                    if_exists = database_modify_value_state,
                    date_type = date_type_value_state,
                )
                
                clean_geoinfo_raw_data_table(
                    engin = engine,
                    table_name_geoinfo = "geoinfo",
                    table_name_raw_data = "raw_data",
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