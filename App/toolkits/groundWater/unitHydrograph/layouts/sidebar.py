from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

NO_MAP_AVAILABLE = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No Map Available ...",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 24}
            }
        ]
    }
}


# -----------------------------------------------------------------------------
# SECTION: TITLE SIDEBAR
# -----------------------------------------------------------------------------
title = html.Div(
    className='text-center py-2 border-bottom border-secondary',
    children=[
        html.H5("محاسبه هیدروگراف واحد")
    ],
)

# -----------------------------------------------------------------------------
# SECTION: BUTTON SIDEBAR
# -----------------------------------------------------------------------------
btn = html.Div(
    className='px-4 py-3 text-center',
    children=[
        html.Div(
            className='row p-0 m-0 ',
            children=[
                html.Div(
                    className='col p-0 px-2 m-0',
                    children=[
                        dbc.Button(
                            id='CALCULATE_UNIT_HYDROGRAPH',
                            className="me-1 w-100",
                            size="md",
                            children=[
                                html.Small(
                                    children=[
                                        '1. محاسبه هیدروگراف'
                                    ],
                                ),
                            ],
                            color='dark',
                            n_clicks=0
                        ),
                    ],
                ),
                html.Div(
                    className='col p-0 px-2 m-0',
                    children=[
                        dbc.Button(
                            id='SHOW_UNIT_HYDROGRAPH',
                            className="me-1 w-100",
                            size="md",
                            children=[
                                html.Small(
                                    children=[
                                        '2. نمایش هیدروگراف'
                                    ],
                                ),
                            ],
                            color='dark',
                            n_clicks=0,
                        )
                    ],
                ),
            ],
        ),
        html.Div(
            id='',
            className='row p-0 m-0 pt-2',
            children=[
                html.Div(
                    className='col p-0 px-2 m-0',
                    children=[
                        dbc.Button(
                            id='SHOW_THIESSEN_MAP',
                            className="me-1 w-100",
                            size="md",
                            children=[
                                html.Small(
                                    children=[
                                        '3. نمایش تیسن‌ها'
                                    ],
                                ),
                            ],
                            color='dark',
                            n_clicks=0,
                        )
                    ],
                ),
                html.Div(
                    className='col p-0 px-2 m-0',
                    children=[
                        dbc.Button(
                            id='SAVE_UNIT_HYDROGRAPH',
                            className="me-1 w-100",
                            size="md",
                            children=[
                                html.Small(
                                    children=[
                                        '4. ذخیره هیدروگراف'
                                    ],
                                ),
                            ],
                            color='dark',
                            n_clicks=0,
                        )
                    ],
                )
            ],
        )
    ],
)

# -----------------------------------------------------------------------------
# SECTION: ACCORDION ITEM - SELECT WELL
# -----------------------------------------------------------------------------
select_well = dmc.AccordionItem(
    label="گام 1: انتخاب آبخوان",
    children=[
        html.Div(
            className='form-group p-3', 
            children=[
                html.Div(
                    className="form-group",
                    children=[
                        html.Div(
                            className="py-2",
                            children=[
                                html.Label(
                                    className='text-center pb-1',
                                    dir='rtl', 
                                    children= [
                                        html.I(className='fas fa-caret-left px-1'),
                                        'محدوده مطالعاتی'
                                    ],
                                    style={
                                        "font-size": "1rem",
                                    }
                                ),
                                dcc.Dropdown(
                                    id='STUDY_AREA_SELECT',
                                    multi=False,
                                    clearable=True,
                                    placeholder='انتخاب محدوده مطالعاتی',
                                ) 
                            ]
                        ),
                        html.Div(
                            className="py-2",
                            children=[
                                html.Label(
                                    className='text-center pb-1',
                                    dir='rtl', 
                                    children=[
                                        html.I(className='fas fa-caret-left px-1'),
                                        'آبخوان',
                                    ],
                                    style={
                                        "font-size": "1rem",
                                    }
                                ),
                                dcc.Dropdown(
                                    id='AQUIFER_SELECT', 
                                    multi=False,
                                    clearable=True,
                                    placeholder='انتخاب آبخوان',
                                )  
                            ]
                        ),
                        html.Div(
                            className="py-2",
                            children=[
                                html.Label(
                                    className='text-center pb-1',
                                    dir='rtl', 
                                    children=[
                                        html.I(className='fas fa-caret-left px-1'),
                                        'چاه‌های مشاهده‌ای'
                                    ],
                                    style={
                                        "font-size": "1rem",
                                    }
                                ),
                                dcc.Dropdown(
                                    id='WELL_SELECT', 
                                    multi=True,
                                    clearable=True,
                                    placeholder='انتخاب چاه‌های مشاهده‌ای',
                                ) 
                            ]
                        ),
                        html.Div(
                            className="py-2",
                            children=[
                                html.Label(
                                    className='text-center pb-1',
                                    dir='rtl', 
                                    children=[
                                        html.I(className='fas fa-caret-left px-1'),
                                        'موقعیت چاه‌های مشاهده‌ای'
                                    ],
                                    style={
                                        "font-size": "1rem",
                                    }
                                ),
                                dcc.Graph(
                                    id='MAP',
                                    figure=NO_MAP_AVAILABLE,
                                    className="border border-secondary p-0 m-0",
                                    style={
                                        "height": "300px",
                                    },
                                )
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)


# -----------------------------------------------------------------------------
# SECTION: ACCORDION ITEM - STORAGE COEFFICIENT
# -----------------------------------------------------------------------------
storage_coefficient = dmc.AccordionItem(
    label="گام 2: انتخاب ضریب ذخیره آبخوان",
    children=[
        html.Div(
            className='form-group p-3', 
            children=[
                html.Div(
                    className="py-2",
                    children=[
                        html.Label(
                            className='text-center pb-2',
                            dir='rtl', 
                            children= [
                                html.I(className='fas fa-caret-left px-1'),
                                'ضریب ذخیره آبخوان'
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        dcc.Input(
                            className="d-block text-center mx-auto",
                            id="STORAGE_COEFFICIENT",
                            type="number",
                            placeholder="آبخوان ...",
                        ) 
                    ]
                ),
            ]
        )
    ]
)

# -----------------------------------------------------------------------------
# SECTION: ACCORDION ITEM - SELECT UNIT HYDROGRAPH METHODS
# -----------------------------------------------------------------------------
unit_hydrograph_method = dmc.AccordionItem(
    label="گام 3: انتخاب روش محاسبه هیدروگراف آبخوان",
    children=[
        html.Div(
            className='form-group p-3', 
            children=[
                html.Div(
                    className="py-2",
                    dir="ltr",
                    children=[
                        html.Label(
                            className='text-center pb-2',
                            dir='rtl', 
                            children= [
                                html.I(className='fas fa-caret-left px-1'),
                                'روش‌های محاسبه هیدروگراف آبخوان'
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        dcc.Checklist(
                            id="UNIT_HYDROGRAPH_METHOD",
                            options=[
                                {"label": "Arithmetic Mean", "value": "AM"},
                                {"label": "Geometric Mean", "value": "GM"},
                                {"label": "Harmonic Mean", "value": "HM"},
                                {"label": "Median", "value": "ME"},
                                {"label": "Thiessen Weighted Average", "value": "TWA"},
                            ],
                            value=["TWA"],
                            labelStyle={"display": "inline-block"},
                            labelClassName="d-flex align-items-center",
                            inputClassName="mx-2",
                            inputStyle={
                                "transform": "scale(1.5)"
                            }
                        ),
                    ]
                ),
            ]
        )
    ]
)



# -----------------------------------------------------------------------------
# SECTION: coordinate reference system
# -----------------------------------------------------------------------------
coordinate_reference_system = dmc.AccordionItem(
    label="گام 4: انتخاب سیستم مختصات مرجع",
    children=[
        html.Div(
            className='form-group p-3', 
            children=[
                html.Div(
                    className="form-group",
                    children=[
                        html.Div(
                            className="py-2",
                            children=[
                                html.Label(
                                    className='text-center pb-1',
                                    dir='rtl', 
                                    children= [
                                        html.I(className='fas fa-caret-left px-1'),
                                        'CRS'
                                    ],
                                    style={
                                        "font-size": "1rem",
                                    }
                                ),
                                dcc.Dropdown(
                                    id='CRS',
                                    multi=False,
                                    clearable=False,
                                    placeholder='انتخاب سیستم مختصات مرجع',
                                    value=3395,
                                    options=[
                                        {'label': 'WGS 84 / World Mercator, EPSG:3395', 'value': 3395},
                                        {'label': 'WGS 84 / UTM Zone 38N, EPSG:32638', 'value': 32638},
                                        {'label': 'WGS 84 / UTM Zone 39N, EPSG:32639', 'value': 32639},
                                        {'label': 'WGS 84 / UTM Zone 40N, EPSG:32640', 'value': 32640},
                                        {'label': 'WGS 84 / UTM Zone 41N, EPSG:32641', 'value': 32641},
                                    ],
                                ) 
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)




# -----------------------------------------------------------------------------
# SECTION: SIDEBAR
# -----------------------------------------------------------------------------
sidebar = html.Div(
    className="m-0 p-0",
    children=[
        title,
        btn,
        html.Div(
            className='form-group p-0 m-0',
            children=[
                dmc.Accordion(
                    class_name="bg-light my-rtl",
                    iconPosition="right",
                    children=[
                        select_well,
                        storage_coefficient,
                        unit_hydrograph_method,
                        coordinate_reference_system
                    ],
                ),
            ],
        ),
    ]
)