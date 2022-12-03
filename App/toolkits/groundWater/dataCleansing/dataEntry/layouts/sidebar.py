from re import A
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc


upload_file = html.Div(
    className='form-group p-3', 
    children=[
        dcc.Upload(
            id="SELECT_FILE",
            accept=".xlsx, .xls",
            children=[
                html.A('انتخاب فایل')
            ], 
            className="select_file_button"
        ),
        html.Div(
            id='SELECT_FILE_NAME',
            children=[
                "فایلی انتخاب نشده است!"
            ],
            className='text-center pt-2 text-danger',
        ),
        dmc.Divider(
            variant="dashed",
        ),
        html.Div(
            className='pt-3 text-center',
            children=[
                html.Div([
                    dbc.Button(
                        "دانلود الگوی فایل ورودی",
                        id="btn_xlsx",
                        color="link"
                    ),
                    dcc.Download(
                        id="download_xlsx"
                    )
                ])
            ],
        ),
        html.Div(
            className='pt-3 text-center',
            children=[
                html.Div([
                    dbc.Button(
                        "نمونه فایل‌های خراسان رضوی",
                        id="btn_mashhad",
                        color="link"
                    ),
                    dcc.Download(
                        id="download_mashhad"
                    )
                ])
            ],
        )
    ]
)

select_worksheet = html.Div(
    className='form-group p-3', 
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Span(
                            children=[
                                "کاربرگ مشخصات"
                            ]
                        ),
                        dcc.Dropdown(
                            id="SELECT_GEOINFO_WORKSHEET",
                            placeholder="انتخاب...",
                            clearable=False
                        )
                    ],
                    className='col-5 p-0 m-0 text-center',
                ),
                html.Div(
                    children=[
                        html.Span(
                            children=[
                                "کاربرگ داده‌ها"
                            ]
                        ),
                        dcc.Dropdown(
                            id="SELECT_DATA_WORKSHEET",
                            placeholder="انتخاب...",
                            clearable=False,
                        )
                    ],
                    className='col-5 p-0 m-0 text-center ',
                ),
            ],
            className='row p-0 m-0 align-items-center justify-content-around',
        ),
    ]
)

database_modify = html.Div(
    className='form-group p-3', 
    children=[
        dcc.RadioItems(
            id='DATABASE_MODIFY', 
            value='replace',
            options=[
                {'label': 'جایگزینی با پایگاه داده خام موجود', 'value': 'replace'},
                {'label': 'به‌روزرسانی پایگاه داده خام موجود', 'value': 'append', 'disabled': True},
            ],
            inputClassName="mx-2",
            labelClassName="my-2",
            labelStyle={'display': 'block'},
        ) 
    ]
)

upload_shapefile = html.Div(
    className='form-group p-3', 
    children=[
        dcc.Upload(
            id="SELECT_SHAPEFILE",
            accept=".zip",
            children=[
                html.A('انتخاب فایل')
            ], 
            className="select_file_button"
        ),
        html.Div(
            id='SELECT_SHAPEFILE_NAME',
            children=[
                "فایلی انتخاب نشده است!"
            ],
            className='text-center pt-2 text-danger',
        )
    ]
)


shapefile_type = html.Div(
    className='form-group p-3 text-center', 
    children=[
        dcc.Dropdown(
            id='SHAPEFILE_TYPE', 
            className="w-100",
            placeholder='لطفا یک مورد انتخاب گردد',
            options=[
                {'label': 'چاه‌های مشاهده‌ای', 'value': 'well'},
                {'label': 'آبخوان‌ها', 'value': 'aquifer'},
                {'label': 'محدوده‌های مطالعاتی', 'value': 'mahdoude'},
            ],
        ) 
    ]
)


geodatabase_modify = html.Div(
    className='form-group p-3', 
    children=[
        dcc.RadioItems(
            id='GEODATABASE_MODIFY', 
            value='append',
            options=[
                {'label': 'جایگزینی با پایگاه داده موجود', 'value': 'replace'},
                {'label': 'به‌روزرسانی پایگاه داده موجود', 'value': 'append'},
            ],
            inputClassName="mx-2",
            labelClassName="my-2",
            labelStyle={'display': 'block'},
        ) 
    ]
)


wt_data = html.Div(
    className="form-group p-0 m-0 pb-3",
    children=[             
        dmc.Accordion(
            class_name="bg-primary my-rtl",
            iconPosition="right",
            children=[
                dmc.AccordionItem(
                    children=[
                        upload_file,
                    ],
                    label="1- انتخاب فایل صفحه گسترده",
                ),
                dmc.AccordionItem(
                    children=[
                        select_worksheet
                    ],
                    label="2- انتخاب کاربرگ",
                    
                ),
                dmc.AccordionItem(
                    children=[
                        database_modify
                    ],
                    label="3- نحوه تغییرات پایگاه داده",
                    
                )
            ],
        ),
        html.Div(
            className='px-5 py-3 text-center',
            children=[
                dbc.Button(
                    id='BUTTON-DATA',
                    className="me-1 w-25",
                    size="md",
                    children='ایجاد', 
                    color='dark',
                    n_clicks=0
                )
            ],
        ),
    ]
)


shapefiles = html.Div(
    className="form-group p-0 m-0",
    children=[             
        dmc.Accordion(
            class_name="bg-primary my-rtl",
            iconPosition="right",
            children=[
                dmc.AccordionItem(
                    children=[
                        upload_shapefile
                    ],
                    label="1- انتخاب شیپ فایل",
                ),
                dmc.AccordionItem(
                    children=[
                        shapefile_type
                    ],
                    label="2- انتخاب نوع شیپ فایل",
                ),
                dmc.AccordionItem(
                    children=[
                        geodatabase_modify
                    ],
                    label="3- نحوه تغییرات پایگاه داده",
                ),
            ],
        ),
        html.Div(
            className='px-5 py-3 text-center',
            children=[
                dbc.Button(
                    id='BUTTON-SHAPEFILES',
                    className="me-1 w-25",
                    size="md",
                    children='ایجاد', 
                    color='dark',
                    n_clicks=0
                )
            ],
        ),
    ]
)






sidebar = html.Div(
    className="m-0 p-0",
    children=[
        
        html.Div(
            className='text-center pb-4',
            children=[
                html.H4("فراخوانی داده‌ها")
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
                                wt_data
                            ],
                            label="مرحله اول: فراخوانی داده‌های سطح آب",
                        ),
                        dmc.AccordionItem(
                            children=[
                                shapefiles
                            ],
                            label="مرحله دوم: فراخوانی شیپ فایل‌ها",
                        ),
                    ],
                ),
            ],
        ),
    ]
)