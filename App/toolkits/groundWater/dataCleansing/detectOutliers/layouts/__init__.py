from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from .body import body
from .sidebar import sidebar
from .navbar import navbar

def layout():
    return html.Div(
        className="m-0 p-0 vh-100 bg-white",
        children=[
            html.Div(
                className="m-0 p-0",
                children=[
                    html.Div(
                        className='p-0 m-0',
                        children=[
                            navbar
                        ],
                    ),
                    html.Div(
                        id='ALERTS',
                    ),
                    html.Div(
                        className='row m-0 p-0 h-body border-top border-1 border-white',
                        
                        children=[
                            html.Div(
                                className='col-3 m-0 p-3 bg-light',
                                children=[
                                    dmc.LoadingOverlay(
                                        children = sidebar,
                                        loaderProps={"variant": "dots", "color": "orange", "size": "xl"},
                                    )
                                ]
                            ),
                            html.Div(
                                className='col-9 m-0 p-3',
                                children=[
                                    dmc.LoadingOverlay(
                                        children = body,
                                        loaderProps={"variant": "dots", "color": "orange", "size": "xl"},
                                    )
                                ]
                            ),
                        ],
                    ),
                ]
            ),
            dcc.Store(
                id='STORAGE',
                storage_type='local',
                data={}
            ),
            dcc.Interval(
                id='INTERVAL',
                interval=1000,
                n_intervals=0,
                max_intervals=1
            ), 
            dcc.Interval(
                id='INTERVAL-STUDYAREA',
                interval=5,
                n_intervals=0,
                max_intervals=1
            ), 
        ]
    )
    
