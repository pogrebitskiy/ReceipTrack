import io
from dash import Dash, dcc, html, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State, dash_table
from dash_bootstrap_templates import load_figure_template
import datetime
from mainj import read_receipt
import base64
from PIL import Image
import plotly.express as px
import pandas as pd
from tabulate import tabulate

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
    html.Div([
        dcc.Graph(id='graph1'),
        dcc.Graph(id='graph2')
    ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top'})

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
@app.callback(Output('output-table-upload', 'children'),
              Output('graph1', 'figure'),
              Output('graph2', 'figure'),
              Input('upload-image', 'contents'))
def update_output(list_of_contents):
    if list_of_contents is not None:
        children = []
        recs = []
        buttons = []
        # Block to display the image, not needed anymore
        '''html.Div([html.Img(src=contents, style={'display': 'inline-block',
                                                 'width': '50%',
                                                 'margin-left': '10px'})]) for contents'''
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

            children.append(html.Hr())
            recs.append(rec)

    # Use the receipt data to bake a bar chart
    prices = [float(rec.total) for rec in recs]
    dates = [pd.to_datetime(rec.date) for rec in recs]

    # Combine entries with the same timestamp
    df = pd.DataFrame({'date': dates, 'price': prices})
    df.sort_values(by=['date'], inplace=True)
    df_grouped = df.groupby(by=['date']).sum().reset_index()

    # JACOB ADDED THIS ----
    category_lst = [category for category in rec.category_dct.keys() for rec in recs]
    price_lst = [price for price in rec.category_dct.values() for rec in recs]
    df_categories = pd.DataFrame({'category': category_lst, 'total': price_lst})
    df_cat_grouped = df_categories.groupby(by=['category']).sum().reset_index()
    print(df_cat_grouped)
    # JACOB ----

    fig1 = px.bar(data_frame=df, x='date', y='price', labels={'date': 'Date', 'price': 'Total'})
    fig2 = px.line(data_frame=df_grouped, x='date', y='price', labels={'date': 'Date', 'price': 'Total'}, markers=True)

    # fig 3 code
    fig3 = px.pie(data_frame = df_cat_grouped, values = 'total', names = 'category')

    return children, fig1, fig2


if __name__ == '__main__':
    app.run_server(debug=False)
