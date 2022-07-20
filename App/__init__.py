from flask import Flask

app = Flask(
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)

app.config["DEBUG"] = True
app.config["UPLOAD_FOLDER"] = "Assets/Files"

from App import routes
