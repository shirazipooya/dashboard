
from dash import html, dcc

body = html.Div(
    [
        html.H6("Change the value in the text box to see callbacks in action!"),
        html.Div(
            [
                "Input: ",
                dcc.Input(id='my-input', value='initial value', type='text')
            ]
        ),
        html.Br(),
        html.Div(id='my-output')
    ]
)