import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
from dash_bootstrap_templates import load_figure_template
import datetime

app = Dash(__name__,
           external_stylesheets=[dbc.themes.LUX, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
           )
load_figure_template('LUX')

app.layout = html.Div([
    html.H1('ReceipTrack', style={'textAlign': 'center'}),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            html.Button('Upload Receipt(s)')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'))
def update_output(list_of_contents):
    if list_of_contents is not None:
        children = [
            html.Div([html.Img(src=contents, style={'display': 'inline-block',
                                                     'width': '50%',
                                                     'margin-left': '10px'})]) for contents
            in list_of_contents]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)
