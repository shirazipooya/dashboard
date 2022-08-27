from re import A
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc


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
            className="me-1 w-50",
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
            className='form-group p-0 m-0 pb-3',
            children=[
                html.H5(
                    children="مرحله اول: چک کردن تاریخ",
                    className="text-center p-2"
                ),     
                
                dmc.Accordion(
                    class_name="bg-light my-rtl",
                    iconPosition="right",
                    children=[
                        dmc.AccordionItem(
                            children=[
                                select_date_type
                            ],
                            label="گام 1: انتخاب فرمت ورودی تاریخ",
                            
                        ),
                        dmc.AccordionItem(
                            children=[
                                action_date
                            ],
                            label="گام 2: نمایش تاریخ‌های اشتباه",
                            
                        ),
                        dmc.AccordionItem(
                            children=[
                                ""
                            ],
                            label="گام 3: اصلاح یا حذف ردیف‌های جدول",
                            
                        ),
                    ],
                ),

                html.Div(
                    className='px-5 py-3 text-center',
                    children=[
                        dbc.Button(
                            id='BUTTON_STAGE_1',
                            className="me-1 w-50",
                            size="md",
                            children='ذخیره تغییرات', 
                            color='dark',
                            n_clicks=0
                        )
                    ],
                )
            ],
        ),

        dmc.Divider(
            variant="solid",
            class_name="pb-3",
            size="md"
        ),  
        
        html.Div(
            className='form-group p-0 m-0 pb-3',
            children=[
                html.H5(
                    children="مرحله دوم: اصلاح دستی داده‌ها",
                    className="text-center p-2"
                ),     
                
                dmc.Accordion(
                    class_name="bg-light my-rtl",
                    iconPosition="right",
                    children=[
                        dmc.AccordionItem(
                            children=[
                                select_well,
                            ],
                            label="گام 1: انتخاب چاه مشاهده‌ای",
                        ),
                        dmc.AccordionItem(
                            children=[
                                extreme_value_check
                            ],
                            label="گام 2: انتخاب حد شناسایی داده‌های پرت",
                        ),
                        dmc.AccordionItem(
                            children=[
                                ""
                            ],
                            label="گام 3: انتخاب نقاط از روی نمودار و اصلاح مقادیر جدول",
                        ),
                    ],
                ),

                html.Div(
                    className='px-5 py-3 text-center',
                    children=[
                        dbc.Button(
                            id='BUTTON_STAGE_2',
                            className="me-1 w-50",
                            size="md",
                            children='ذخیره تغییرات', 
                            color='dark',
                            n_clicks=0
                        )
                    ],
                )
            ],
        ),
    ]
)