import numpy as np
import pandas as pd
import sqlalchemy as sa
import plotly.graph_objects as go
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from App.db import POSTGRES_USER_NAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


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
                "font": {"size": 36}
            }
        ]
    }
}

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
# DATABASE CONNECTION: data
# -----------------------------------------------------------------------------
POSTGRES_DB_NAME = "data"
TABLE_NAME_RAW_DATA = "raw_data"
TABLE_NAME_MODIFIED_DATA = "modified_data"
TABLE_NAME_INTERPOLATED_DATA = "interpolated_data"

db = f"postgresql://{POSTGRES_USER_NAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"
engine = sa.create_engine(db, echo=False)


# -----------------------------------------------------------------------------
# DATABASE CONNECTION: layers
# -----------------------------------------------------------------------------
POSTGRES_DB_LAYERS = "layers"
db_layers = f"postgresql://{POSTGRES_USER_NAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_LAYERS}"
engine_layers = sa.create_engine(db_layers, echo=False)


# -----------------------------------------------------------------------------
# FUNCTION INTERPOLATION
# -----------------------------------------------------------------------------
def f_interpolate(
    df,
    method,
    order,
    limit,
    time_scale="monthly"
):
    if time_scale == "monthly":
        
        cols_p = ['YEAR_PERSIAN', 'MONTH_PERSIAN', 'DAY_PERSIAN']                        
        cols_g = ['YEAR_GREGORIAN', 'MONTH_GREGORIAN', 'DAY_GREGORIAN']
        
        persian_date_min = df["DATE_PERSIAN"].min()                     
        persian_date_max = df["DATE_PERSIAN"].max()        
        persian_date_min_list = persian_date_min.split("-")
        persian_date_max_list = persian_date_max.split("-")
        
        year = list(range(int(persian_date_min_list[0]), int(persian_date_max_list[0]) + 1))
        month = list(range(1, 13))        
        tmp = pd.DataFrame(
            {
                "YEAR_PERSIAN": np.repeat(year, 12, axis=0),
                "MONTH_PERSIAN": month * len(year)
            }
        )        
        tmp["YEAR_PERSIAN"] = tmp["YEAR_PERSIAN"].astype(str).str.zfill(4)
        tmp["MONTH_PERSIAN"] = tmp["MONTH_PERSIAN"].astype(str).str.zfill(2)
        
        df = pd.merge(left=df, right=tmp, on=["YEAR_PERSIAN", "MONTH_PERSIAN"], how="outer").reset_index(drop=True)
                
        df["MAHDOUDE"] = df["MAHDOUDE"].interpolate(method="pad")
        df["AQUIFER"] = df["AQUIFER"].interpolate(method="pad")
        df["LOCATION"] = df["LOCATION"].interpolate(method="pad")
        df["DAY_PERSIAN"] = df["DAY_PERSIAN"].interpolate(method="pad")
        
        df[cols_p] = df[cols_p].apply(pd.to_numeric, errors='coerce')
        df[cols_p] = df[cols_p].astype(pd.Int64Dtype())
        
        date_persian, date_gregorian = np.vectorize(ymd_persian_to_date)(df.YEAR_PERSIAN, df.MONTH_PERSIAN, df.DAY_PERSIAN)
        
        df["DATE_PERSIAN"] = list(date_persian)
        df["DATE_GREGORIAN"] = list(date_gregorian)
        
        df[cols_p] = df['DATE_PERSIAN'].str.split('-', 2, expand=True)
        df[cols_g] = df['DATE_GREGORIAN'].astype(str).str.split('-', 2, expand=True)
        
        df["YEAR_PERSIAN"] = df["YEAR_PERSIAN"].astype(str).str.zfill(4)
        df["MONTH_PERSIAN"] = df["MONTH_PERSIAN"].astype(str).str.zfill(2)
        df["DAY_PERSIAN"] = df["DAY_PERSIAN"].astype(str).str.zfill(2)
        df["YEAR_GREGORIAN"] = df["YEAR_GREGORIAN"].str.zfill(4)
        df["MONTH_GREGORIAN"] = df["MONTH_GREGORIAN"].str.zfill(2)
        df["DAY_GREGORIAN"] = df["DAY_GREGORIAN"].str.zfill(2)
        df['DATE_PERSIAN'] = df["YEAR_PERSIAN"] + "-" + df["MONTH_PERSIAN"] + "-" + df["DAY_PERSIAN"]
        df['DATE_GREGORIAN'] = df["YEAR_GREGORIAN"] + "-" + df["MONTH_GREGORIAN"] + "-" + df["DAY_GREGORIAN"]
        df["DATE_GREGORIAN"] = df["DATE_GREGORIAN"].apply(pd.to_datetime)
        
        df = df.sort_values(
            by=["MAHDOUDE", "AQUIFER", "LOCATION", "DATE_GREGORIAN"]
        )
        
        df = df.loc[(df['DATE_PERSIAN'] >= persian_date_min) & (df['DATE_PERSIAN'] <= persian_date_max)]
        
        df = df.reset_index(drop=True)
        
        if method in ["polynomial", "spline"]:
            if limit == 0:
                df["WATER_TABLE"] = df["WATER_TABLE"].interpolate(method=method, order=order)
            else:
                df["WATER_TABLE"] = df["WATER_TABLE"].interpolate(method=method, order=order, limit=limit)
        else:
            if limit == 0:
                df["WATER_TABLE"] = df["WATER_TABLE"].interpolate(method=method)
            else:
                df["WATER_TABLE"] = df["WATER_TABLE"].interpolate(method=method, limit=limit)
        
        return df
    
    else:
        
        return None


# -----------------------------------------------------------------------------
# FUNCTION CONVERT DAY, MONTH, YEAR PERSIAN TO DATE
# -----------------------------------------------------------------------------
def ymd_persian_to_date(
    year,
    month,
    day,
):
    try:
        date_persian = str(year) + "-" + str(month) + "-" + str(day)
        date_gregorian = JalaliDate(year, month, day).to_gregorian()
        return date_persian, date_gregorian
    except:
        return pd.NA, pd.NA