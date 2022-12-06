import io
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, dash_table
from dash_bootstrap_templates import load_figure_template
import datetime
from main import read_receipt
import base64
from PIL import Image
import plotly.express as px
import pandas as pd
from tabulate import tabulate

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
    ), html.Div([
        dcc.Interval(id='progress-interval', n_intervals=0, interval=500),
        dbc.Progress(id='progress')
    ]),
    # Allocate space for graphs and tables
    html.Div(id='output-table-upload', style={'width': '45%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='graph1'),
        dcc.Graph(id='graph2'),

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


# Combined callback for the file upload and graphing
@app.callback(Output('progress', 'value'),
              Output('progress', 'label'),
              Output('output-table-upload', 'children'),
              Output('graph1', 'figure'),
              Output('graph2', 'figure'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              Input('progress-interval', 'n_intervals')
              )
def update_output(list_of_contents, list_of_names,n):
    if list_of_contents is not None:
        children = []
        recs = []
        buttons = []
        # Block to display the image, not needed anymore
        '''html.Div([html.Img(src=contents, style={'display': 'inline-block',
                                                 'width': '50%',
                                                 'margin-left': '10px'})]) for contents'''
        progress = 0
        for i in range(len(list_of_contents)):
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
            progress = min(i/len(list_of_contents), 100)

        tabs = dbc.Accordion(
            [dbc.AccordionItem(table, title=list_of_names[children.index(table)]) for table in children],
            )

    # Use the receipt data to bake a bar chart
    try:
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

        return progress, f"{progress} %" if progress >= 5 else "", tabs, fig1, fig2

    except:
        pass
if __name__ == '__main__':
    app.run_server(debug=False)
