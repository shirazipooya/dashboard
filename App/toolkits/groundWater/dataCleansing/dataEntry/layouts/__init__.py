from dash import html

from .body import body
from .sidebar import sidebar
from .navbar import navbar

def layout():
    return html.Div(
        className="m-0 p-0",
        children=[
            html.Div(
                className="row m-0 p-0",
                children=[
                    navbar
                ]
            )
        ]
    )