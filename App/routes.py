from flask import render_template
from App import app

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


@app.route('/groundwater/datacleansing')
def groundwater_dataCleansing():
    return render_template(
        template_name_or_list="groundwater_dataCleansing.html"
    )


@app.route('/groundwater/datavisualization')
def groundwater_dataVisualization():
    return render_template(
        template_name_or_list="groundwater_dataVisualization.html"
    )


@app.route('/groundwater/dataCleansing/dataEntry')
def groundWater_dataCleansing_dataEntry():
    return app.index()


@app.route('/groundwater/dataCleansing/detectOutliers')
def groundWater_dataCleansing_detectOutliers():
    return app.index()