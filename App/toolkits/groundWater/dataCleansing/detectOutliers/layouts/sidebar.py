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
                            multi=True,
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
                            multi=True,
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
                            multi=True,
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
                {'label': 'تاریخ شمسی با فرمت "01-01-1400"', 'value': 'persian_date', 'disabled': True},
                {'label': 'تاریخ شمسی با فرمت سال، ماه و روز', 'value': 'persian_ymd', 'disabled': False},
                {'label': 'تاریخ میلادی با فرمت "01-01-2020"', 'value': 'gregorian_date', 'disabled': True},
                {'label': 'تاریخ میلادی با فرمت سال، ماه و روز', 'value': 'gregorian_ymd', 'disabled': True},
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
                html.H2("شناسایی داده‌های پرت")
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
                                dmc.Accordion(
                                    class_name="bg-primary my-rtl",
                                    iconPosition="right",
                                    children=[
                                        dmc.AccordionItem(
                                            children=[
                                                select_date_type
                                            ],
                                            label="1- انتخاب فرمت ورودی تاریخ",
                                            
                                        ),
                                        dmc.AccordionItem(
                                            children=[
                                                action_date
                                            ],
                                            label="2- نمایش تاریخ‌های اشتباه",
                                            
                                        ),
                                        dmc.AccordionItem(
                                            children=[
                                                html.Div(
                                                    className='px-1 py-3 text-center',
                                                    children=[
                                                        "از جدول «ردیف‌ها با تاریخ اشتباه» تاریخ‌های نمایش داده شده را اصلاح یا با کلیک بر روی علامت ضربدر آن ردیف را حذف کنید و در ادامه روی «ذخیره تغییرات» و سپس «تنظیم تاریخ» کلیک نمایید."
                                                    ],
                                                )
                                            ],
                                            label="3- اصلاح یا حذف ردیف‌های جدول",

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
                                                    id='BUTTON_STAGE_1',
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
                                                dbc.Button(
                                                    id='BUTTON_DATE',
                                                    className="me-1 w-100",
                                                    size="md",
                                                    children='تبدیل تاریخ', 
                                                    color='dark',
                                                    n_clicks=0,
                                                )
                                            ],
                                        )
                                    ],
                                )
                            ],
                            label="مرحله اول: چک کردن تاریخ",
                        ),
                        dmc.AccordionItem(
                            children=[
                                dmc.Accordion(
                                    class_name="bg-primary my-rtl",
                                    iconPosition="right",
                                    children=[
                                        dmc.AccordionItem(
                                            children=[
                                                select_well,
                                            ],
                                            label="1- انتخاب چاه مشاهده‌ای",
                                        ),
                                        dmc.AccordionItem(
                                            children=[
                                                extreme_value_check
                                            ],
                                            label="2- انتخاب حد شناسایی داده‌های پرت",
                                        ),
                                        dmc.AccordionItem(
                                            children=[
                                                html.Div(
                                                    className='px-1 py-3 text-center',
                                                    children=[
                                                        "با استفاده از ابزار انتخاب نمودار، داده‌هایی که نیاز به اصلاح دارند را انتخاب و در جدول نمایش داده شده، داده‌های انتخابی را اصلاح کنید. پس از انجام تغییرات روی «ذخیره تغییرات» کلیک نمایید."
                                                    ],
                                                )
                                            ],
                                            label="3- انتخاب نقاط از روی نمودار و اصلاح مقادیر جدول",
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
                            label="مرحله دوم: اصلاح دستی داده‌ها",
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
                            label="مرحله سوم: دانلود‌ داده‌های اصلاح شده",
                        ),
                    ]
                )
            ]
        )
    ]
)