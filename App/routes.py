from flask import render_template
from App import app
from flask import render_template

@app.route("/")
def home():
    return render_template(
        template_name_or_list="home.html"
    )


@app.route('/groundwater')
def groundwater():
    return render_template(
        template_name_or_list="groundwater.html"
    )