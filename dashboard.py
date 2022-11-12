import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
from dash_bootstrap_templates import load_figure_template

app = Dash(__name__,
           external_stylesheets=[dbc.themes.LUX, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
           )
load_figure_template('LUX')

app.layout = html.Div([
    html.H1('ReceipTrack', style={'textAlign': 'center'}),
    html.Hr(),
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
        }
    ),
    html.Div(id='output-image-upload'),
])


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'))
def update_output(image):
    if image is not None:
        children = [
            html.Div([html.Center(html.Img(src=image, style={'width': '40%',
                                                             'height': '40%',
                                                             'textAlign': 'center'}))])
        ]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)
