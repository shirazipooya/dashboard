import itertools
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import voronoi_diagram as svd
from shapely.wkt import loads as load_wkt
import sqlalchemy as sa
import psycopg2
import plotly.graph_objects as go
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from App.db import *


# -----------------------------------------------------------------------------
# CONSTANT VARIABLES
# -----------------------------------------------------------------------------
NO_MATCHING_GRAPH_FOUND = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No Graph Found ...",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 24}
            }
        ]
    }
}

NO_MATCHING_MAP_FOUND = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No Map Found ...",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 24}
            }
        ]
    }
}

NO_MATCHING_TABLE_FOUND = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No Table Found ...",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 24}
            }
        ]
    }
}

# -----------------------------------------------------------------------------
# MAPBOX TOKEN
# -----------------------------------------------------------------------------
PATH_MAPBOX_TOKEN = "./Assets/.mapbox_token"
MAPBOX_TOKEN = open(PATH_MAPBOX_TOKEN).read()



# -----------------------------------------------------------------------------
# BASE MAP
# -----------------------------------------------------------------------------
BASE_MAP = go.Figure(
    go.Scattermapbox(
        
    )
)

BASE_MAP.update_layout(
    mapbox={
        'style': "stamen-terrain",
        'center': {
            'lon': 59.55,
            'lat': 36.25
        },
        'zoom': 5.5
    },
    showlegend=False,
    hovermode='closest',
    margin={'l':0, 'r':0, 'b':0, 't':0},
    autosize=False
)


# -----------------------------------------------------------------------------
# READ STORAGE COEFFICIENT
# -----------------------------------------------------------------------------
modify_cols=['MAHDOUDE', 'AQUIFER']
STORAGE_COEFFICIENT = pd.read_csv("./Assets/Files/STORAGE_COEFFICIENT.csv")
STORAGE_COEFFICIENT[modify_cols] = STORAGE_COEFFICIENT[modify_cols].apply(lambda x: x.str.rstrip())
STORAGE_COEFFICIENT[modify_cols] = STORAGE_COEFFICIENT[modify_cols].apply(lambda x: x.str.lstrip())
STORAGE_COEFFICIENT[modify_cols] = STORAGE_COEFFICIENT[modify_cols].apply(lambda x: x.str.replace('ي','ی'))
STORAGE_COEFFICIENT[modify_cols] = STORAGE_COEFFICIENT[modify_cols].apply(lambda x: x.str.replace('ئ','ی'))
STORAGE_COEFFICIENT[modify_cols] = STORAGE_COEFFICIENT[modify_cols].apply(lambda x: x.str.replace('ك', 'ک'))

# -----------------------------------------------------------------------------
# FUNCTION: FIND TABLE
# -----------------------------------------------------------------------------
def find_table(
    database,
    table,
    user,
    password,
    host,
    port,
):
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    conn.autocommit = True    
    cursor = conn.cursor()    
    sql = '''SELECT table_name FROM information_schema.tables;'''
    cursor.execute(sql)
    table_name_list_exist = list(itertools.chain.from_iterable(cursor.fetchall()))
    conn.close()
    
    if table in table_name_list_exist:
        return True
    else:
        return False

# -----------------------------------------------------------------------------
# FUNCTION: BASIC FUNCTION TO REMOVE / DROP / FILL THE HOLES.
# -----------------------------------------------------------------------------
def dropHolesBase(plg):
	'''
	BASIC FUNCTION TO REMOVE / DROP / FILL THE HOLES.
	PARAMETERS:
		plg: plg WHO HAS HOLES / EMPTIES.
			Type: shapely.geometry.MultiPolygon OR shapely.geometry.Polygon
	RETURNS:
		A shapely.geometry.MultiPolygon OR shapely.geometry.Polygon object
	'''
	if isinstance(plg, MultiPolygon):
		return MultiPolygon(Polygon(p.exterior) for p in plg)
	elif isinstance(plg, Polygon):
		return Polygon(plg.exterior)

# -----------------------------------------------------------------------------
# FUNCTION: REMOVE / DROP / FILL THE HOLES / EMPTIES FOR ITERMS IN GeoDataFrame
# -----------------------------------------------------------------------------
def dropHoles(gdf):
	'''
	REMOVE / DROP / FILL THE HOLES / EMPTIES FOR ITERMS IN GeoDataFrame.	
	PARAMETERS:
		gdf:
			Type: geopandas.GeoDataFrame
	RETURNS:
		gdf_nohole: GeoDataFrame WITHOUT HOLES
			Type: geopandas.GeoDataFrame	
	'''
	gdf_nohole = gpd.GeoDataFrame()
	for g in gdf['geometry']:
		geo = gpd.GeoDataFrame(geometry=gpd.GeoSeries(dropHolesBase(g)))
		gdf_nohole=gdf_nohole.append(geo,ignore_index=True)
	gdf_nohole.rename(columns={gdf_nohole.columns[0]:'geometry'}, inplace=True)
	gdf_nohole.crs = gdf.crs
	gdf.rename(columns={'geometry': 'geometry_old'}, inplace=True)
	gdf["geometry_new"] = gdf_nohole
	gdf.rename(columns={'geometry_new': 'geometry'}, inplace=True)
	gdf.drop(['geometry_old'], axis=1, inplace=True)
	return gdf

# -----------------------------------------------------------------------------
# FUNCTION: THIESSEN POLYGONS
# -----------------------------------------------------------------------------    
def thiessen_polygons(gdf, mask):
    gdf.reset_index(drop=True)
    # CONVERT TO shapely.geometry.MultiPolygon
    smp = gdf.unary_union
    # CREATE PRIMARY VORONOI DIAGRAM BY INVOKING shapely.ops.voronoi_diagram
    poly = load_wkt('POLYGON ((42 24, 64 24, 64 42, 42 42, 42 24))')
    smp_vd = svd(smp, envelope=poly)
    # CONVERT TO GeoSeries AND explode TO SINGLE POLYGONS
    gs = gpd.GeoSeries([smp_vd]).explode()
    # CONVERT TO GEODATAFRAME
    # NOTE THAT IF GDF WAS shapely.geometry.MultiPolygon, IT HAS NO ATTRIBUTE 'crs'
    gdf_vd_primary = gpd.geodataframe.GeoDataFrame(geometry=gs, crs=gdf.crs)	
    # RESET INDEX
    gdf_vd_primary.reset_index(drop=True)
    gdf_vd_primary = gpd.clip(gdf_vd_primary, mask)	
    
    # SPATIAL JOIN BY INTERSECTING AND DISSOLVE BY `index_right`
    gdf_temp = (gpd.sjoin(gdf_vd_primary, gdf, how='inner', op='intersects').dissolve(by='index_right').reset_index(drop=True))
    # gdf_vd = gpd.clip(gdf_temp, mask)
    # gdf_vd = dropHoles(gdf_vd)
    return gdf_temp

# -----------------------------------------------------------------------------
# FUNCTION: CALCULATE THIESSEN POLYGONS
# -----------------------------------------------------------------------------
def calculate_thiessen_polygons(
    data,
    para,
    point,
    point_name,
    limit
):

    data = data.dropna(subset=[para]).reset_index(drop=True)      
    point = point[point[point_name].isin(data[point_name].unique())]  
    point['POINT_IS_IN_LIMIT'] = point['geometry'].apply(lambda x: limit.contains(x))   
    point = point[point['POINT_IS_IN_LIMIT']].reset_index(drop=True)
        
    if len(point) > 0:
        
        vd = thiessen_polygons(gdf=point, mask=limit)
        vd.set_geometry(col='geometry', inplace=True)
        vd["THISSEN_POINT"] = vd.geometry.area / 1000 / 1000
        vd["THISSEN_LIMIT"] = [limit.geometry.area[0] / 1000 / 1000] * len(point)
        vd = vd[[
			point_name, 'THISSEN_POINT', 'THISSEN_LIMIT', 'geometry'
		]]
                
        return vd
    
    else:
        
        return gpd.GeoDataFrame()

# -----------------------------------------------------------------------------
# FUNCTION: CHECK THIESSEN CHANGE
# -----------------------------------------------------------------------------
def check_thiessen_change(df):
    df = df.reset_index(drop=True)
    CHECK_LOCATION_CONDI = []
    for i, l in enumerate(df.LOCATION_LIST):
        if i == 0:
            CHECK_LOCATION_CONDI.append(False)
        elif set(df.LOCATION_LIST[i]) == set(df.LOCATION_LIST[i-1]):
            CHECK_LOCATION_CONDI.append(False)
        else:
            CHECK_LOCATION_CONDI.append(True)
    df["THISSEN_CHANGE"] = CHECK_LOCATION_CONDI
    return df

def check_persian_date_ymd(
    year_persian,
    month_persian,
    day_persian,
):
    try:
        date_persian = str(year_persian) + "-" + str(month_persian) + "-" + str(day_persian)
        date_gregorian = JalaliDate(year_persian, month_persian, day_persian).to_gregorian()
        return date_persian, date_gregorian
    except:
        return pd.NA, pd.NA