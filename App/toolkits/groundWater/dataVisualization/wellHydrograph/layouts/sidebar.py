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
        html.H4("نمایش هیدروگراف چاه مشاهده‌ای")
    ],
)


# -----------------------------------------------------------------------------
# SECTION: ACCORDION ITEM - SELECT WELL
# -----------------------------------------------------------------------------
select_well = dmc.AccordionItem(
    label="گام 1: انتخاب چاه مشاهده‌ای",
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
                        select_well,
                        date
                    ],
                ),
            ],
        ),
    ]
)