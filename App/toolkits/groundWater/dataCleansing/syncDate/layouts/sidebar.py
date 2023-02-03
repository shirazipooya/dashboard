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
                                    options=[{"label": "بدون تغییر", "value": 0}] + [{"label": day, "value": day} for day in range(1,31)],
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
                                    options=[{"label": "بدون تغییر", "value": 0}] + [{"label": day, "value": day} for day in range(1,31)],
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
                                'هماهنگ‌سازی تاریخ برای:',
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

sidebar = html.Div(
    className="m-0 p-0",
    children=[
        
        html.Div(
            className='text-center pb-4',
            children=[
                html.H4("هماهنگ‌سازی تاریخ")
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
                            label="مرحله اول- انتخاب چاه مشاهده‌ای",
                        ),
                        dmc.AccordionItem(
                            children=[
                                compare_days
                            ],
                            label="مرحله دوم- مقایسه روزهای مختلف",
                        ),
                        dmc.AccordionItem(
                            children=[
                                save_sync_date_result
                            ],
                            label="مرحله سوم- ذخیره داده‌های هماهنگ‌سازی شده",
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
                            label="مرحله چهارم- دانلود‌ داده‌های هماهنگ‌سازی شده",
                        ),
                    ],
                ),
            ],
        ),
    ]
)