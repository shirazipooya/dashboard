from dash.dependencies import Output, Input, State

def toolkits__groundWater__dataCleansing__dataEntry__callbacks(app):
    
    @app.callback(
        Output(component_id='my-output', component_property='children'),
        Input(component_id='my-input', component_property='value')
    )
    def my_func(input_value):
        return f'Output: {input_value}'