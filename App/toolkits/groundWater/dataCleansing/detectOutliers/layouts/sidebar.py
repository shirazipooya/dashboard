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

action_type = html.Div(
    className='form-group p-3', 
    children=[
        dcc.RadioItems(
            id='ACTION_TYPE', 
            value='manual',
            options=[
                {'label': 'دستی', 'value': 'manual'},
                {'label': 'خودکار', 'value': 'automatic', 'disabled': True},
            ],
            inputClassName="mx-2",
            labelClassName="my-2",
            labelStyle={'display': 'block'},
            style={
                'display': 'flex',
                'justify-content': 'space-around'
            },
        ) 
    ]
)


sidebar = html.Div(
    className="m-0 p-0",
    children=[
         html.H5(
             children="شناسایی داده‌های پرت",
             className="text-center p-2"
        ),
         
        dmc.Divider(
            variant="solid",
            class_name="pb-3",
            size="md"
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
                        action_type
                    ],
                    label="گام 3: انتخاب روش اصلاح داده‌ها",
                    
                ),
            ],
        ),

        html.Div(
            className='px-5 py-3 text-center',
            children=[
                dbc.Button(
                    id='BUTTON',
                    className="me-1 w-50",
                    size="md",
                    children='ذخیره تغییرات', 
                    color='dark',
                    n_clicks=0
                )
            ],
        )

    ]
)