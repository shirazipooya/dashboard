from flask import Flask
from .toolkits.groundWater.dataCleansing.dataEntry.app import toolkits__groundWater__dataCleansing__dataEntry
from .toolkits.groundWater.dataCleansing.detectOutliers.app import toolkits__groundWater__dataCleansing__detectOutliers
from .db import *

app = Flask(
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)

app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = "Assets/Files"

toolkits__groundWater__dataCleansing__dataEntry(server=app)
toolkits__groundWater__dataCleansing__detectOutliers(server=app)

from App import routes
