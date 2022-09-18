import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, MultiplexerTransform, LogTransform

from .callbacks.callbacks import toolkits__groundWater__dataVisualization__aquiferHydrograph__callbacks
from .layouts import layout

external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "/static/vendor/fontawesome/v6.1.1/css/all.css",
    "/static/vendor/bootstrap/v5.2.0/css/bootstrap.min.css",
    "/static/vendor/bootstrap-icons/v1.9.1/bootstrap-icons.css",
    "/static/vendor/animate/v4.1.1/animate.min.css",
    "/static/css/main.css",
]

external_scripts=[
    "/static/vendor/jquery/v3.6.0/jquery.min.js",
    "/static/vendor/popper/v2.9.2/popper.min.js",
    "/static/vendor/bootstrap/v5.2.0/js/bootstrap.min.js",
]

def toolkits__groundWater__dataVisualization__aquiferHydrograph(server):
    
    toolkits__groundWater__dataVisualization__aquiferHydrograph__app = DashProxy(
        transforms=[MultiplexerTransform(), LogTransform()],
        name="toolkits__groundWater__dataVisualization__aquiferHydrograph",
        server=server,
        url_base_pathname="/groundwater/dataVisualization/aquiferHydrograph/",
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts,
        title='نمایش هیدروگراف واحد آبخوان',
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True
    )
    
    toolkits__groundWater__dataVisualization__aquiferHydrograph__app.layout = layout()
    
    toolkits__groundWater__dataVisualization__aquiferHydrograph__callbacks(app=toolkits__groundWater__dataVisualization__aquiferHydrograph__app)
    
    return toolkits__groundWater__dataVisualization__aquiferHydrograph__app