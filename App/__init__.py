from flask import Flask
from .toolkits.groundWater.dataCleansing.dataEntry.app import toolkits__groundWater__dataCleansing__dataEntry
from .toolkits.groundWater.dataCleansing.detectOutliers.app import toolkits__groundWater__dataCleansing__detectOutliers
from .toolkits.groundWater.dataCleansing.interpolation.app import toolkits__groundWater__dataCleansing__interpolation
from .toolkits.groundWater.dataCleansing.syncDate.app import toolkits__groundWater__dataCleansing__syncDate
from .toolkits.groundWater.unitHydrograph.app import toolkits__groundWater__unitHydrograph
from .toolkits.groundWater.dataVisualization.wellHydrograph.app import toolkits__groundWater__dataVisualization__wellHydrograph
from .toolkits.groundWater.dataVisualization.aquiferHydrograph.app import toolkits__groundWater__dataVisualization__aquiferHydrograph
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
toolkits__groundWater__dataCleansing__interpolation(server=app)
toolkits__groundWater__dataCleansing__syncDate(server=app)
toolkits__groundWater__unitHydrograph(server=app)
toolkits__groundWater__dataVisualization__wellHydrograph(server=app)
toolkits__groundWater__dataVisualization__aquiferHydrograph(server=app)

from App import routes
