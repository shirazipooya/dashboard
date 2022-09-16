from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc

NO_MATCHING_GRAPH_FOUND = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No Graph Found ...",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 24}
            }
        ]
    }
}

NO_MATCHING_MAP_FOUND = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No Map Found ...",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 24}
            }
        ]
    }
}

NO_MATCHING_TABLE_FOUND = {
    "layout": {
        "xaxis": {"visible": False},
        "yaxis": {"visible": False},
        "annotations": [
            {
                "text": "No Table Found ...",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 24}
            }
        ]
    }
}

body = html.Div(
    className="m-0 p-0 text-center",
    style={"height": "85vh"},
    children=[
        html.Div(
            hidden=False,
            className='row p-0 m-0 border border-light border-bottom-0',
            style={"--bs-border-width": "10px"},
            children=[
                html.Div(
                    id='UNIT_HYDROGRAPH_GRAPH',
                    children=[
                        dcc.Graph(
                            figure=NO_MATCHING_GRAPH_FOUND
                        )
                    ],
                    className='col p-0 m-0 w-100',
                    dir="rtl"
                )
            ]
        ),
        html.Div(
            hidden=False,
            className='row p-0 m-0 border border-light border-bottom-0',
            style={"--bs-border-width": "10px"},
            children=[
                html.Div(
                    id='UNIT_HYDROGRAPH_TABLE',
                    children=[
                        dcc.Graph(
                            figure=NO_MATCHING_TABLE_FOUND
                        )
                    ],
                    className='col p-0 m-0 w-100',
                    dir="rtl"
                )
            ]
        ),
        html.Div(
            hidden=False,
            className='row p-0 m-0',
            children=[
                html.Div(
                    id='THIESSEN_MAP',
                    children=[
                        dcc.Graph(
                            figure=NO_MATCHING_MAP_FOUND
                        )
                    ],
                    className='col-4 p-0 m-0 border border-light  border-start-0',
                    style={"--bs-border-width": "10px"},
                    dir="rtl"
                ),
                html.Div(
                    id='THIESSEN_GRAPH',
                    children=[
                        dcc.Graph(
                            figure=NO_MATCHING_GRAPH_FOUND
                        )
                    ],
                    className='col-8 p-0 m-0 border border-light',
                    style={"--bs-border-width": "10px"},
                    dir="rtl"
                ),
            ]
        )
    ]
)