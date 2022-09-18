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
    className='text-center pb-4',
    children=[
        html.H4("نمایش هیدروگراف واحد آبخوان")
    ],
)


# -----------------------------------------------------------------------------
# SECTION: ACCORDION ITEM - SELECT AQUIFER
# -----------------------------------------------------------------------------
select_aquifer = dmc.AccordionItem(
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
                                        'موقعیت آبخوان'
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
# SECTION: ACCORDION ITEM - DATE
# -----------------------------------------------------------------------------
date = dmc.AccordionItem(
    label="گام 2: انتخاب بازه زمانی",
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
                                'شروع'
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className='row m-0 p-0',
                            children=[
                                html.Div(
                                    className='col p-0 m-0 px-1 text-center',
                                    children=[
                                        dcc.Dropdown(
                                            id='START_MONTH',
                                            clearable=True,
                                            placeholder="ماه",
                                        ) 
                                    ],
                                ),
                                html.Div(
                                    className='col p-0 m-0 px-1 text-center',
                                    children=[
                                        dcc.Dropdown(
                                            id='START_YEAR',
                                            clearable=True,
                                            placeholder="سال",
                                        ) 
                                    ],
                                )
                                
                            ],
                        )
                    ]
                ),
                html.Div(
                    className="py-2",
                    children=[
                        html.Label(
                            className='text-center pb-2',
                            dir='rtl', 
                            children= [
                                html.I(className='fas fa-caret-left px-1'),
                                'پایان'
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className='row m-0 p-0',
                            children=[
                                html.Div(
                                    className='col p-0 m-0 px-1 text-center',
                                    children=[
                                        dcc.Dropdown(
                                            id='END_MONTH',
                                            clearable=True,
                                            placeholder="ماه",
                                        ) 
                                    ],
                                ),
                                html.Div(
                                    className='col p-0 m-0 px-1 text-center',
                                    children=[
                                        dcc.Dropdown(
                                            id='END_YEAR',
                                            clearable=True,
                                            placeholder="سال",
                                        ) 
                                    ],
                                )
                                
                            ],
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
    label="گام 3: انتخاب روش محاسبه هیدروگراف",
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
                        dcc.RadioItems(
                            id="UNIT_HYDROGRAPH_METHOD",
                            options=[
                                {"label": "Arithmetic Mean", "value": "AM", "disabled": True},
                                {"label": "Geometric Mean", "value": "GM", "disabled": True},
                                {"label": "Harmonic Mean", "value": "HM", "disabled": True},
                                {"label": "Median", "value": "ME", "disabled": True},
                                {"label": "Thiessen Weighted Average", "value": "TWA", "disabled": True},
                            ],
                            value="TWA",
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
# SECTION: ACCORDION ITEM - SELECT UNIT HYDROGRAPH METHODS
# -----------------------------------------------------------------------------
unit_hydrograph_para = dmc.AccordionItem(
    label="گام 4: انتخاب متغییر",
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
                                'انتخاب متغییر نمایش'
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        dcc.RadioItems(
                            id="UNIT_HYDROGRAPH_PARA",
                            style={
                                "direction": "rtl"    
                            },
                            options=[
                                {"label": "تغییرات تراز سطح آب", "value": "WL"},
                                {"label": "تغییرات ذخیره مخزن", "value": "SR"},
                            ],
                            value="WL",
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
# SECTION: SIDEBAR
# -----------------------------------------------------------------------------
sidebar = html.Div(
    className="m-0 p-0",
    children=[
        title,
        html.Div(
            className='form-group p-0 m-0',
            children=[
                dmc.Accordion(
                    class_name="bg-light my-rtl",
                    iconPosition="right",
                    children=[
                        select_aquifer,
                        date,
                        unit_hydrograph_method,
                        unit_hydrograph_para
                    ],
                ),
            ],
        ),
    ]
)