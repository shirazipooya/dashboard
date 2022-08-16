from dash import html
import dash_bootstrap_components as dbc

body = html.Div(
    className="m-0 p-0",
    children=[
        html.Div(
            className='row p-0 m-0 ',
            children=[
                html.Div(
                    className='col-6 p-0 m-0 text-center',
                    children=[
                        dbc.Button(
                            id='GEOINFO_TABLE_BUTTON',
                            className="w-50",
                            size="lg",
                            children='نمایش جدول مشخصات', 
                            color='dark',
                            n_clicks=0
                        )
                    ],
                ),
                html.Div(
                    className='col-6 p-0 m-0 text-center',
                    children=[
                        dbc.Button(
                            id='RAW_DATA_TABLE_BUTTON',
                            className="w-50",
                            size="lg",
                            children='نمایش جدول داده‌ها', 
                            color='dark',
                            n_clicks=0
                        )
                    ],
                )
            ],
        ),
        html.Div(
            # id='TABLE',
            className='row p-5 m-0',
            children=[
                html.Div(
                    id='TABLE',
                    className='col p-0 m-0 w-100',
                )
            ]
        ),
    ]
)