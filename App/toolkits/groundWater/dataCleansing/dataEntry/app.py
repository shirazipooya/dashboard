import dash
import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, MultiplexerTransform, LogTransform

from .callbacks.callbacks import toolkits__groundWater__dataCleansing__dataEntry__callbacks
from .layouts import layout

external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "/static/vendor/fontawesome/v6.1.1/css/all.css",
    "/static/vendor/bootstrap/v5.2.0/css/bootstrap.min.css",
    "/static/vendor/animate/v4.1.1/animate.min.css",
    "/static/css/main.css",
]

external_scripts=[
    "/static/vendor/jquery/v3.6.0/jquery.min.js",
    "/static/vendor/popper/v2.9.2/popper.min.js",
    "/static/vendor/bootstrap/v5.2.0/js/bootstrap.min.js",
]

def toolkits__groundWater__dataCleansing__dataEntry(server):
    
    toolkits__groundWater__dataCleansing__dataEntry__app = DashProxy(
        transforms=[MultiplexerTransform(), LogTransform()],
        name="toolkit__dataEntry__dataCleansing__groundWater",
        server=server,
        url_base_pathname="/groundwater/dataCleansing/dataEntry/",
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts,
        title='فراخوانی داده‌ها',
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True
    )
    
    toolkits__groundWater__dataCleansing__dataEntry__app.layout = layout()
    
    toolkits__groundWater__dataCleansing__dataEntry__callbacks(app=toolkits__groundWater__dataCleansing__dataEntry__app)
    
    return toolkits__groundWater__dataCleansing__dataEntry__app