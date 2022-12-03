from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'd3946e1cf4b2b53d4dcf5d9e3b126498ac2876892270735eddbb7e3aca8a7bbe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../Assets/users.db'

db_users = SQLAlchemy(app=app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app=app)
login_manager.login_view = 'login'
login_manager.login_message = 'لطفاً ابتدا وارد بشوید!'
login_manager.login_message_category = "info"

toolkits__groundWater__dataCleansing__dataEntry(server=app)
toolkits__groundWater__dataCleansing__detectOutliers(server=app)
toolkits__groundWater__dataCleansing__interpolation(server=app)
toolkits__groundWater__dataCleansing__syncDate(server=app)
toolkits__groundWater__unitHydrograph(server=app)
toolkits__groundWater__dataVisualization__wellHydrograph(server=app)
toolkits__groundWater__dataVisualization__aquiferHydrograph(server=app)

@app.before_first_request
def create_tables():
    db_users.create_all()

from App import routes
