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
                    className="py-2",
                    children=[
                        html.Label(
                            className='text-center pb-1',
                            dir='rtl', 
                            children= [
                                html.I(className='fas fa-caret-left px-1'),
                                'انتخاب روش بازسازی داده‌ها'
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
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
                            clearable=False
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
                                'انتخاب مرتبه',
                            ],
                            style={
                                "font-size": "1rem",
                            }
                        ),
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
                            multi=True,
                            placeholder='انتخاب چاه مشاهده‌ای',
                        ) 
                    ]
                ),
            ]
        )
    ]
)





extreme_value_check = html.Div(
    className='form-group p-3', 
    children=[
        html.Div(
            className="row py-1 m-0 align-items-center justify-content-around",
            children=[
                html.Div(
                    className='col-9 p-0 m-0',
                    children=[
                        html.Label(
                            className='text-center align-items-center',
                            dir='rtl', 
                            children=[
                                html.I(className='fas fa-caret-left px-1'),
                                'روش میانگین',
                            ]
                        )
                    ],
                ),
                html.Div(
                    className='col-3 p-0 m-0 text-center',
                    children=[
                        dcc.Dropdown(
                            id='MEAN_METHOD', 
                            value=4,
                            options=[{"label": f"{x}x", "value": x} for x in [i for i in range(1, 11)]],
                            clearable=False
                        ) 
                    ],
                )
            ]
        ),
        html.Div(
            className="row py-1 m-0 align-items-center justify-content-around",
            children=[
                html.Div(
                    className='col-9 p-0 m-0',
                    children=[
                        html.Label(
                            className='text-center align-items-center',
                            dir='rtl', 
                            children=[
                                html.I(className='fas fa-caret-left px-1'),
                                'روش مشتق',
                            ]
                        )
                    ],
                ),
                html.Div(
                    className='col-3 p-0 m-0 text-center',
                    children=[
                        dcc.Dropdown(
                            id='DERIVATIVE_METHOD',
                            value=4,
                            options=[{"label": f"{x}%", "value": x} for x in [i for i in range(1, 11)]],
                            clearable=False
                        ) 
                    ],
                )
            ]
        ),
    ]
)


action_date = html.Div(
    className='form-group p-3 text-center', 
    children=[
        dbc.Button(
            id='BUTTON_SHOW_WRONG_DATE',
            className="me-1",
            size="md",
            children='نمایش تاریخ‌های اشتباه', 
            color='dark',
            outline=True,
            n_clicks=0
        )
    ]
)


action_type = html.Div(
    className='form-group p-3', 
    children=[
        dcc.Checklist(
            className="row",
            id='ACTION_TYPE', 
            value=['date', 'zeros'],
            options=[
                {'label': 'اصلاح تاریخ‌های اشتباه', 'value': 'date', 'disabled': True},
                {'label': 'حذف مقادیر صفر سطح ایستابی', 'value': 'zeros', 'disabled': False},
            ],
            inputClassName="mx-2",
            labelClassName="my-2",
            inline=False
        ) 
    ]
)

select_date_type = html.Div(
    className='form-group p-3', 
    children=[
        dcc.RadioItems(
            id='SELECT_DATE_TYPE', 
            value='persian_ymd',
            options=[
                {'label': 'تاریخ شمسی با فرمت "01-01-1400"', 'value': 'persian_date'},
                {'label': 'تاریخ شمسی با فرمت سال، ماه و روز', 'value': 'persian_ymd'},
                {'label': 'تاریخ میلادی با فرمت "01-01-2020"', 'value': 'gregorian_date'},
                {'label': 'تاریخ میلادی با فرمت سال، ماه و روز', 'value': 'gregorian_ymd'},
            ],
            inputClassName="mx-2",
            labelClassName="my-2",
            labelStyle={'display': 'block'},
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

        dmc.Divider(
            variant="solid",
            class_name="pb-3",
            size="sm"
        ),  
        
        html.Div(
            className='form-group p-0 m-0 pb-3',
            children=[
                dmc.Accordion(
                    class_name="bg-light my-rtl",
                    iconPosition="right",
                    children=[
                        dmc.AccordionItem(
                            children=[
                                select_well
                            ],
                            label="1- انتخاب چاه مشاهده‌ای",
                        ),
                        dmc.AccordionItem(
                            children=[
                                compare_methods
                            ],
                            label="2- مقایسه روش‌های مختلف بازسازی",
                        ),
                        dmc.AccordionItem(
                            children=[
                                
                            ],
                            label="3- ذخیره داده‌های بازسازی شده",
                        ),
                    ],
                ),
                html.Div(
                    className='row px-5 py-3 text-center',
                    children=[
                        html.Div(
                            className='col p-0 px-2 m-0',
                            children=[
                                dbc.Button(
                                    id='BUTTON_TABLE_GRAPH',
                                    className="me-1 w-100",
                                    size="md",
                                    children='ذخیره تغییرات', 
                                    color='dark',
                                    n_clicks=0
                                ),
                            ],
                        ),
                        html.Div(
                            className='col p-0 px-2 m-0',
                            children=[
                                html.A(
                                    children = 
                                        dbc.Button(
                                            className="me-1 w-100",
                                            size="md",
                                            children='بارگذاری صفحه', 
                                            color='dark',
                                            n_clicks=0
                                        ),
                                    href='/groundwater/dataCleansing/detectOutliers/'
                                ) 
                            ],
                        )
                    ],
                )
            ],
        ),
    ]
)