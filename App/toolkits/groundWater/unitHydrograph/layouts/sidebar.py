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



compare_days = html.Div(
    className='form-group p-3', 
    children=[
        html.Div(
            className="form-group",
            children=[
                html.Div(
                    className="form-group inline m-0 my-1 d-flex align-items-center",
                    style={
                        'display': 'flex',
                    },
                    children=[
                        html.Label(
                            className='text-right m-0',
                            dir='rtl', 
                            children='تبدیل به روز',
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className='w-50',
                            children=[
                                dcc.Dropdown(
                                    id='SYNC_DAY',
                                    value=15,
                                    options=[
                                        {"label": day, "value": day} for day in range(1,31)
                                    ],
                                    multi=False,
                                    clearable=False,
                                    className="mx-3"
                                ),
                            ],
                        ),
                        html.Label(
                            className='text-center m-0',
                            dir='rtl', 
                            children='هر ماه',
                            style={
                                "font-size": "1rem",
                            }
                        ),

                    ]
                ),
                html.Div(
                    className='row px-5 pt-3 text-center',
                    children=[
                        html.Div(
                            className='col p-0 px-2 m-0',
                            children=[
                                dbc.Button(
                                    id='SYNC_DATE_BUTTON',
                                    className="me-1 w-50",
                                    size="md",
                                    children='مقایسه', 
                                    color='dark',
                                    n_clicks=0
                                ),
                            ],
                        )
                    ],
                )
            ]
        )
    ]
)


save_sync_date_result = html.Div(
    className='form-group p-3', 
    children=[
        html.Div(
            className="form-group",
            children=[
                html.Div(
                    className="form-group inline m-0 my-1 d-flex align-items-center",
                    style={
                        'display': 'flex',
                    },
                    children=[
                        html.Label(
                            className='text-right m-0',
                            dir='rtl', 
                            children='تبدیل به روز',
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className='w-50',
                            children=[
                                dcc.Dropdown(
                                    id='SAVE_SYNC_DAY',
                                    value=15,
                                    options=[
                                        {"label": day, "value": day} for day in range(1,31)
                                    ],
                                    multi=False,
                                    clearable=False,
                                    className="mx-3"
                                ),
                            ],
                        ),
                        html.Label(
                            className='text-center m-0',
                            dir='rtl', 
                            children='هر ماه',
                            style={
                                "font-size": "1rem",
                            }
                        ),

                    ]
                ),
                html.Div(
                    className="form-group inline m-0 my-1 pt-2",
                    style={
                        # 'display': 'flex',
                        # 'justify-content': 'space-between',
                        'align-items': 'center'
                    },
                    children=[
                        html.Label(
                            className='text-center',
                            dir='rtl', 
                            children=[
                                html.I(className='fas fa-caret-left px-1'),
                                'بازسازی داده‌های مفقودی برای:',
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className="w-100 p-0 m-0 pt-1 text-center",
                            children=[
                                dcc.Dropdown(
                                    id='SAVE_WHICH_WELL',
                                    clearable=True,
                                    placeholder="انتخاب روش‌ ...",
                                    options=[
                                        {'label': 'همه چاه‌های مشاهده‌ای', 'value': 0},
                                    ]
                                ) 
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='row px-5 pt-3 text-center',
                    children=[
                        html.Div(
                            className='col p-0 px-2 m-0',
                            children=[
                                dbc.Button(
                                    id='SAVE_SYNC_DATE_BUTTON',
                                    className="me-1",
                                    size="md",
                                    children='ذخیره محاسبات', 
                                    color='dark',
                                    n_clicks=0
                                ),
                            ],
                        )
                    ],
                )
            ]
        )
    ]
)

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
    className='row px-4 py-3 text-center',
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
                                'محاسبه هیدروگراف'
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
                    id='SAVE_UNIT_HYDROGRAPH',
                    className="me-1 w-100",
                    size="md",
                    children=[
                        html.Small(
                            children=[
                                'ذخیره هیدروگراف'
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

# -----------------------------------------------------------------------------
# SECTION: ACCORDION ITEM - SELECT WELL
# -----------------------------------------------------------------------------
select_well = dmc.AccordionItem(
    label="1- انتخاب چاه‌های مشاهده‌ای",
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
                                    multi=False,
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
                    ],
                ),
            ],
        ),
    ]
)