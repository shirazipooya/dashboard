from dash import html
import dash_bootstrap_components as dbc


navbar = html.Nav(
    className="navbar navbar-expand-lg navbar-dark bg-dark",
    style={
        "height": "56px"
    },
    children=[
        html.Div(
            className="container-fluid w-90",
            children=[
                html.Div(
                    id='navbarResponsive',
                    className='collapse navbar-collapse',
                    children=[
                        html.Ul(
                            className='navbar-nav ml-auto pr-4', 
                            children=[
                                html.Li(
                                    className='nav-item active', 
                                    children=[
                                        html.A(
                                            className='nav-link navbar-brand link-hover text-white', 
                                            children="خانه",
                                            href='/',
                                        )
                                    ]
                                ),
                                html.Li(
                                    className='nav-item active', 
                                    children=[
                                        html.A(
                                            className='nav-link navbar-brand link-hover text-white', 
                                            children="مصورسازی داده‌ها",
                                            href='/groundwater/datavisualization',
                                        )
                                    ]
                                ),
                                # html.Li(
                                #     className='nav-item active', 
                                #     children=[
                                #         html.A(
                                #             className='nav-link navbar-brand link-hover text-white', 
                                #             children="آب زیرزمینی",
                                #             href='/groundwater',
                                #         )
                                #     ]
                                # ),
                                # html.Li(
                                #     className='nav-item active', 
                                #     children=[
                                #         html.A(
                                #             className='disabled nav-link navbar-brand link-hover text-muted', 
                                #             children="آب سطحی",
                                #             href='/',
                                #         )
                                #     ]
                                # ),
                                # html.Li(
                                #     className='nav-item active', 
                                #     children=[
                                #         html.A(
                                #             className='disabled nav-link navbar-brand link-hover text-muted', 
                                #             children="پایش کیفی",
                                #             href='/',
                                #         )
                                #     ]
                                # ),
                            ]
                        )
                    ],
                ),
                html.A(
                    className='navbar-brand mr-auto pl-4',
                    children="شرکت سهامی آب منطقه‌ای خراسان رضوی",
                    href='http://www.khrw.ir/'
                )
            ]
        )
    ]
)