from dash import html
import dash_bootstrap_components as dbc

body = html.Div(
    className="m-0 p-0",
    style={"height": "85vh"},
    children=[
        html.Div(
            className='row p-0 m-0 text-center',
            children=[
                html.Div(
                    className='col p-0 px-1 m-0 text-center',
                    children=[
                        dbc.Button(
                            id='GEOINFO_TABLE_BUTTON',
                            className="w-100",
                            children='نمایش جدول مشخصات', 
                            color='dark',
                            n_clicks=0
                        )
                    ],
                ),
                html.Div(
                    className='col p-0 px-1 m-0 text-center',
                    children=[
                        dbc.Button(
                            id='RAW_DATA_TABLE_BUTTON',
                            className="w-100",
                            children='نمایش جدول داده‌ها', 
                            color='dark',
                            n_clicks=0
                        )
                    ],
                ),
                html.Div(
                    className='col p-0 px-1 m-0 text-center',
                    children=[
                        dbc.Button(
                            id='STUDY_AREA_MAP_BUTTON',
                            className="w-100",
                            children='نمایش محدوده‌های مطالعاتی', 
                            color='dark',
                            n_clicks=0
                        )
                    ],
                ),
                html.Div(
                    className='col p-0 px-1 m-0 text-center',
                    children=[
                        dbc.Button(
                            id='AQUIFER_MAP_BUTTON',
                            className="w-100",
                            children='نمایش آبخوان‌ها', 
                            color='dark',
                            n_clicks=0
                        )
                    ],
                ),
                html.Div(
                    className='col p-0 px-1 m-0 text-center',
                    children=[
                        dbc.Button(
                            id='WELL_MAP_BUTTON',
                            className="w-100",
                            children='نمایش چاه‌های مشاهده‌ای', 
                            color='dark',
                            n_clicks=0
                        )
                    ],
                ),
            ],
        ),
        html.Div(
            className='row py-3 px-1 m-0 h-100',
            children=[
                html.Div(
                    id='CONTENT',
                    className='col p-0 m-0 w-100 text-center',
                    dir="rtl"
                )
            ]
        ),
    ]
)