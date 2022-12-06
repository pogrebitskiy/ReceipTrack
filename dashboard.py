import io
import sys

import matplotlib.pyplot as plt
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, dash_table, exceptions
from dash_bootstrap_templates import load_figure_template
import datetime
from main import read_receipt
import base64
from PIL import Image
import plotly.express as px
import pandas as pd
from tabulate import tabulate
from tqdm import tqdm
import subprocess
import plotly.graph_objects as go


subprocess.check_call(([sys.executable, "-m", "pip", "install", "tqdm"]))
subprocess.check_call(([sys.executable, "-m", "pip", "install", "dash-bootstrap-components"]))


def blank_figure():
    """Function to show blank page instead of graph axis"""
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig

# Create dash app with themes to look good
app = Dash(__name__,
           external_stylesheets=[dbc.themes.LUMEN, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
           )
load_figure_template('LUMEN')
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
    html.Div([
        # Component to display upload progress
        dbc.Progress(id='pbar', striped=True, animated=True,style={
            'width': '100%',
            'height': '20px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderRadius': '5px',
            'margin': '10px',
        } ),
        # Component to increment time and auto-update
        dcc.Interval(id='timer_progress')]),
    # Allocate space for graphs and tables
    html.Div(id='output-table-upload', style={'width': '45%', 'display': 'inline-block'}),
    html.Div([dbc.Tabs([
        dbc.Tab(dcc.Graph(id='graph1', figure=blank_figure()), label='Pie Chart'),
        dbc.Tab(dcc.Graph(id='graph2', figure=blank_figure()), label='Bar Chart'),
    ])
    ], style={'width': '55%', 'display': 'inline-block', 'verticalAlign': 'top', 'height': '80%'})

])


@app.callback(
    Output({'type': 'collapse-table', 'index': MATCH}, 'is_open'),
    [Input({'type': 'collapse-button', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'collapse-table', 'index': MATCH}, 'is_open')]
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('pbar', 'value'),
    Output('pbar', 'label'),
    Input('timer_progress', 'n_intervals'),
    prevent_initial_call=True
)
def _callback_progress(n_intervals):
    """Reads in the progress of the main callback from a file"""
    try:
        # Read the file and find the percentage value
        with open('progress.txt', 'r') as file:
            str_raw = file.read()
        last_line = list(filter(None, str_raw.split('\n')))[-1]
        percent = float(last_line.split('%')[0])
    except:
        # Set value to 0 if not found
        percent = 0

    finally:
        # Return value and formatted string
        text = f'{percent:.0f}%'
        return percent, text


# Combined callback for the file upload and graphing
@app.callback(
    Output('output-table-upload', 'children'),
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename'),
    prevent_initial_call=True
)
def _update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = []
        recs = []
        buttons = []
        # Block to display the image, not needed anymore
        '''html.Div([html.Img(src=contents, style={'display': 'inline-block',
                                                 'width': '50%',
                                                 'margin-left': '10px'})]) for contents'''

        # Open progress file
        file_prog = open('progress.txt', 'w')
        # Loop runs with tqdm which tracks progress of a for loop and outputs progress to file
        for i in tqdm(range(len(list_of_contents)), file=file_prog):
            # Split encoded string
            content_type, content_string = list_of_contents[i].split(',')
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
                                                             html.Tr([html.Td('Total'), html.Td(rec.total)])]
                                                            )
                                                 ]),
                                      dbc.CardHeader(dbc.Button('List of Items',
                                                                id={'type': 'collapse-button', 'index': i})),
                                      dbc.Collapse(dbc.CardBody(dbc.Table.from_dataframe(rec.item_df, striped=True)),
                                                   id={'type': 'collapse-table', 'index': i}, is_open=False)],
                                     style={'margin-left': '10px'}))

            recs.append(rec)

        # Clear the file and close it
        file_prog.truncate(0)
        file_prog.close()


        tabs = dbc.Accordion(
            [dbc.AccordionItem(table, title=list_of_names[children.index(table)]) for table in children],
        )

        # Use the receipt data to bake a bar chart
        prices = [float(rec.total) for rec in recs]
        dates = [pd.to_datetime(rec.date) for rec in recs]

        # Combine entries with the same timestamp
        df = pd.DataFrame({'date': dates, 'price': prices})
        df.sort_values(by=['date'], inplace=True)
        df_grouped = df.groupby(by=['date']).sum().reset_index()

        # Create dictionary with unique categories as keys and total price for the value
        cat = {}
        for rec in recs:
            for key, value in rec.category_dct.items():
                if key in cat.keys():
                    cat[key] += value
                else:
                    cat[key] = value
        df_categories = pd.DataFrame({'category': list(cat.keys()), 'total': list(cat.values())})
        df_categories = df_categories[df_categories['category'] != 'other']

        fig1 = px.pie(data_frame=df_categories, values='total', names='category')
        fig2 = px.bar(data_frame=df, x='date', y='price', labels={'date': 'Date', 'price': 'Total'})



        return tabs, fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=False)
