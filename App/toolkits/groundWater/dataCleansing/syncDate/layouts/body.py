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

table_error_date = dash_table.DataTable(
    id="TABLE_ERROR_DATE",
    editable=True,
    row_deletable=True,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    sort_by=[
        {"column_id": "MAHDOUDE", "direction": "asc"},
        {"column_id": "AQUIFER", "direction": "asc"},
        {"column_id": "LOCATION", "direction": "asc"},
    ],
    page_size=12,
    style_as_list_view=True,
    style_table={
        'overflowX': 'auto',
        'overflowY': 'auto',
        'direction': 'rtl',
    },
    style_cell={
        'font-family': "Vazir-Regular-FD",
        'border': '1px solid grey',
        'font-size': '14px',
        'text_align': 'center',
        'minWidth': 150,
        'maxWidth': 200,
    },
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'border':'1px solid grey',
        'fontWeight': 'bold',
        'text_align': 'center',
        'height': 'auto',
    },
    style_data={
        'color': 'black',
        'backgroundColor': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(245, 245, 245)',
        }
    ]
)




body = html.Div(
    className="m-0 p-0 text-center",
    style={"height": "85vh"},
    children=[
        html.Div(
            id="DIV_GRAPH",
            hidden=False,
            className='row p-1 m-0',
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id='GRAPH',
                            figure=NO_MATCHING_GRAPH_FOUND
                        )
                    ],
                    className='col p-0 m-0 w-100',
                    dir="rtl"
                )
            ]
        ),
        html.Div(
            id="DIV_GRAPH_SYNCHRONIZED",
            hidden=True,
            className='row p-1 m-0',
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id='GRAPH_SYNCHRONIZED',
                            figure=NO_MATCHING_GRAPH_FOUND
                        )
                    ],
                    className='col p-0 m-0 w-100',
                    dir="rtl"
                )
            ]
        )
    ]
)