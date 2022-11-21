import io

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, dash_table
from dash_bootstrap_templates import load_figure_template
import datetime
from main import read_receipt
import base64
from PIL import Image
import plotly.express as px
import pandas as pd

# Create dash app with themes to look good
app = Dash(__name__,
           external_stylesheets=[dbc.themes.LUX, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
           )
load_figure_template('LUX')


# Build the layout of the app
app.layout = html.Div([
    html.H1('ReceipTrack', style={'textAlign': 'center'}),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            html.Button('Upload Receipts')
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
    # Allocate space for graphs and tables
    html.Div(id='output-table-upload', style={'width': '40%', 'display': 'inline-block'}),
    dcc.Graph(id='graph1', style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top'})


])

# Combined callback for the file upload and graphing
@app.callback(Output('output-table-upload', 'children'),
              Output('graph1', 'figure'),
              Input('upload-image', 'contents'))
def update_output(list_of_contents):
    if list_of_contents is not None:
        children = []
        recs = []
        # Block to display the image, not needed anymore
        '''html.Div([html.Img(src=contents, style={'display': 'inline-block',
                                                 'width': '50%',
                                                 'margin-left': '10px'})]) for contents'''
        for rec in list_of_contents:
            # Split encoded string
            content_type, content_string = rec.split(',')
            rec = content_string

            # Decode the string back to an image
            img = Image.open(io.BytesIO(base64.b64decode(rec)))
            img.save('temp.jpg')

            # Read the re-decoded image
            rec = read_receipt('temp.jpg')



            # Create a table from the receipt
            children.append(html.Div([dbc.Table([html.Tbody([html.Tr([html.Td('Date'), html.Td(rec.date)]),
                                                             html.Tr([html.Td('Phone Number'), html.Td(rec.phone)]),
                                                             html.Tr([html.Td('Subtotal'), html.Td(rec.subtotal)]),
                                                             html.Tr([html.Td('Total'), html.Td(rec.total)]),
                                                             html.Tr([html.Td('Change Due'), html.Td(rec.change)])])])],
                                     style={'margin-left':'10px'}))
            children.append(html.Hr())
            recs.append(rec)

    # Use the receipt data to bake a bar chart
    prices = [float(rec.total) for rec in recs]
    dates = [pd.to_datetime(rec.date) for rec in recs]
    fig1 = px.bar(x=dates, y=prices, labels={'x':'Date', 'y':'Total'})

    return children, fig1

if __name__ == '__main__':
    app.run_server(debug=False)
