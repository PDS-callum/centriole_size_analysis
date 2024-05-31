from dash import dcc, html, Input, Output, Dash
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import glob
import re

filename_mask = ""

# Assuming the function annotate_images is defined elsewhere
from utils.general_utils import *

circles_data_df = pd.read_csv("test.csv")

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Label("Enter filename:"),
    dcc.Input(id="filename-input", type="text"),
    dcc.Graph(id='my-graph')
])

# Callback function to update the histogram based on user input
@app.callback(
    Output(component_id="my-graph", component_property="figure"),
    Input(component_id="filename-input", component_property="value"),
)
def update_histogram(filename_mask):
    r = re.compile(filename_mask)
    set_filenames = list(set(circles_data_df.filename.values))
    matching_filenames = list(filter(r.match, set_filenames))
    print(matching_filenames)
    fig = go.Figure()
    for filename in matching_filenames:
        query_df = circles_data_df.query("filename == @filename")
        fig.add_trace(
            go.Histogram(
                x=query_df.radius,
                name=filename
            )
        )
    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
