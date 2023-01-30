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

select_well = html.Div(
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
                                'چاه مشاهده‌ای'
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        dcc.Dropdown(
                            id='WELL_SELECT', 
                            multi=False,
                            clearable=True,
                            placeholder='انتخاب چاه مشاهده‌ای',
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
                                'موقعیت چاه مشاهده‌ای'
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

compare_methods = html.Div(
    className='form-group p-3', 
    children=[
        html.Div(
            className="form-group",
            children=[
                html.Div(
                    className="form-group inline m-0 my-1",
                    style={
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'align-items': 'center'
                    },
                    children=[
                        html.Label(
                            className='text-center',
                            dir='rtl', 
                            children=[
                                html.I(className='fas fa-caret-left px-1'),
                                'انتخاب روش‌ها',
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className="w-50 p-0 m-0",
                            children=[
                                dcc.Dropdown(
                                    id='INTERPOLATE_METHODS',
                                    multi=True,
                                    placeholder="انتخاب روش‌ها ...",
                                    options=[
                                        {'label': 'Back Fill', 'value': 'bfill'},
                                        {'label': 'Forward Fill', 'value': 'ffill'},
                                        {'label': 'Pad', 'value': 'pad'},
                                        {'label': 'Zero', 'value': 'zero'},
                                        {'label': 'Linear', 'value': 'linear'},
                                        {'label': 'Slinear', 'value': 'slinear'},
                                        {'label': 'Akima', 'value': 'akima'},
                                        {'label': 'Nearest', 'value': 'nearest'},
                                        {'label': 'Spline', 'value': 'spline'},
                                        {'label': 'Polynomial', 'value': 'polynomial'},
                                        {'label': 'Cubic', 'value': 'cubic'},
                                        {'label': 'Quadratic', 'value': 'quadratic'},
                                        {'label': 'Barycentric', 'value': 'barycentric'},
                                        {'label': 'Krogh', 'value': 'krogh'},
                                        {'label': 'Piecewise Polynomial', 'value': 'piecewise_polynomial'},
                                        {'label': 'Pchip', 'value': 'pchip'},
                                        {'label': 'Cubicspline', 'value': 'cubicspline'},
                                    ],
                                    clearable=True
                                ) 

                            ]
                        )
                    ]
                ),
                html.Div(
                    className="form-group inline m-0 my-1",
                    style={
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'align-items': 'center'
                    },
                    children=[
                        html.Label(
                            className='text-center',
                            dir='rtl', 
                            children=[
                                html.I(className='fas fa-caret-left px-1'),
                                'انتخاب مرتبه',
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className="w-50 p-0 m-0 text-center",
                            children=[
                                dcc.Dropdown(
                                    id='ORDER_INTERPOLATE_METHODS', 
                                    value=1,
                                    disabled=True,
                                    options=[
                                        {'label': '0', 'value': 0},
                                        {'label': '1', 'value': 1},
                                        {'label': '2', 'value': 2},
                                        {'label': '3', 'value': 3},
                                        {'label': '4', 'value': 4},
                                        {'label': '5', 'value': 5},
                                    ],
                                    clearable=False
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="form-group inline m-0 my-1",
                    style={
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'align-items': 'center'
                    },
                    children=[
                        html.Label(
                            className='text-center',
                            dir='rtl', 
                            children=[
                                html.I(className='fas fa-caret-left px-1'),
                                'انتخاب تعداد ماه‌',
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className="w-50 p-0 m-0 text-center",
                            children=[
                                dcc.Dropdown(
                                    id='NUMBER_MONTHS', 
                                    value=0,
                                    options=[
                                        {'label': 'بدون محدودیت', 'value': 0},
                                        {'label': '1', 'value': 1},
                                        {'label': '2', 'value': 2},
                                        {'label': '3', 'value': 3},
                                        {'label': '4', 'value': 4},
                                        {'label': '6', 'value': 6},
                                        {'label': '9', 'value': 9},
                                        {'label': '12', 'value': 12},
                                        {'label': '15', 'value': 15},
                                        {'label': '18', 'value': 18},
                                        {'label': '21', 'value': 21},
                                        {'label': '24', 'value': 24},
                                    ],
                                    clearable=False
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
                                    id='INTERPOLATE_BUTTON',
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


save_interpolate_result = html.Div(
    className='form-group p-3', 
    children=[
        html.Div(
            className="form-group",
            children=[
                html.Div(
                    className="form-group inline m-0 my-1",
                    style={
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'align-items': 'center'
                    },
                    children=[
                        html.Label(
                            className='text-center',
                            dir='rtl', 
                            children=[
                                html.I(className='fas fa-caret-left px-1'),
                                'انتخاب روش‌',
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className="w-50 p-0 m-0",
                            children=[
                                dcc.Dropdown(
                                    id='SAVE_INTERPOLATE_METHODS',
                                    multi=False,
                                    placeholder="انتخاب روش‌ ...",
                                    options=[
                                        {'label': 'Back Fill', 'value': 'bfill'},
                                        {'label': 'Forward Fill', 'value': 'ffill'},
                                        {'label': 'Pad', 'value': 'pad'},
                                        {'label': 'Zero', 'value': 'zero'},
                                        {'label': 'Linear', 'value': 'linear'},
                                        {'label': 'Slinear', 'value': 'slinear'},
                                        {'label': 'Akima', 'value': 'akima'},
                                        {'label': 'Nearest', 'value': 'nearest'},
                                        {'label': 'Spline', 'value': 'spline'},
                                        {'label': 'Polynomial', 'value': 'polynomial'},
                                        {'label': 'Cubic', 'value': 'cubic'},
                                        {'label': 'Quadratic', 'value': 'quadratic'},
                                        {'label': 'Barycentric', 'value': 'barycentric'},
                                        {'label': 'Krogh', 'value': 'krogh'},
                                        {'label': 'Piecewise Polynomial', 'value': 'piecewise_polynomial'},
                                        {'label': 'Pchip', 'value': 'pchip'},
                                        {'label': 'Cubicspline', 'value': 'cubicspline'},
                                    ],
                                    clearable=True
                                ) 

                            ]
                        )
                    ]
                ),
                html.Div(
                    className="form-group inline m-0 my-1",
                    style={
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'align-items': 'center'
                    },
                    children=[
                        html.Label(
                            className='text-center',
                            dir='rtl', 
                            children=[
                                html.I(className='fas fa-caret-left px-1'),
                                'انتخاب مرتبه',
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className="w-50 p-0 m-0 text-center",
                            children=[
                                dcc.Dropdown(
                                    id='SAVE_ORDER_INTERPOLATE_METHODS', 
                                    value=1,
                                    disabled=True,
                                    options=[
                                        {'label': '0', 'value': 0},
                                        {'label': '1', 'value': 1},
                                        {'label': '2', 'value': 2},
                                        {'label': '3', 'value': 3},
                                        {'label': '4', 'value': 4},
                                        {'label': '5', 'value': 5},
                                    ],
                                    clearable=False
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className="form-group inline m-0 my-1",
                    style={
                        'display': 'flex',
                        'justify-content': 'space-between',
                        'align-items': 'center'
                    },
                    children=[
                        html.Label(
                            className='text-center',
                            dir='rtl', 
                            children=[
                                html.I(className='fas fa-caret-left px-1'),
                                'انتخاب تعداد ماه‌',
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
                        html.Div(
                            className="w-50 p-0 m-0 text-center",
                            children=[
                                dcc.Dropdown(
                                    id='SAVE_NUMBER_MONTHS', 
                                    value=0,
                                    options=[
                                        {'label': 'بدون محدودیت', 'value': 0},
                                        {'label': '1', 'value': 1},
                                        {'label': '2', 'value': 2},
                                        {'label': '3', 'value': 3},
                                        {'label': '4', 'value': 4},
                                        {'label': '6', 'value': 6},
                                        {'label': '9', 'value': 9},
                                        {'label': '12', 'value': 12},
                                        {'label': '15', 'value': 15},
                                        {'label': '18', 'value': 18},
                                        {'label': '21', 'value': 21},
                                        {'label': '24', 'value': 24},
                                    ],
                                    clearable=False
                                ) 
                            ]
                        )
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
                                    id='SAVE_INTERPOLATE_BUTTON',
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

sidebar = html.Div(
    className="m-0 p-0",
    children=[
        
        html.Div(
            className='text-center pb-4',
            children=[
                html.H4("بازسازی داده‌های مفقودی سطح آب")
            ],
        ),
        
        html.Div(
            className='form-group p-0 m-0 pb-3',
            children=[
                dmc.Accordion(
                    class_name="bg-dark my-rtl",
                    iconPosition="right",
                    children=[
                        dmc.AccordionItem(
                            children=[
                                select_well
                            ],
                            label="مرحله اول: انتخاب چاه مشاهده‌ای",
                        ),
                        dmc.AccordionItem(
                            children=[
                                compare_methods
                            ],
                            label="مرحله دوم: مقایسه روش‌های مختلف بازسازی",
                        ),
                        dmc.AccordionItem(
                            children=[
                                save_interpolate_result
                            ],
                            label="مرحله سوم: ذخیره داده‌های بازسازی شده",
                        ),
                        dmc.AccordionItem(
                            children=[
                                html.Div(
                                    className='row px-5 py-3 text-center',
                                    children=[
                                        html.Div(
                                            className='col p-0 px-2 m-0',
                                            children=[
                                                html.Button("دانلود داده‌ها", id="BTN_XLSX", className="btn btn-dark btn-md"),
                                                dcc.Download(id="DOWNLOAD_XLSX")
                                            ],
                                        ),
                                    ],
                                )
                            ],
                            label="مرحله چهارم: دانلود‌ داده‌های بازسازی شده",
                        ),
                    ],
                ),
            ],
        ),
    ]
)