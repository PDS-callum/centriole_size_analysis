import argparse
import cv2
import pandas as pd
import os
import numpy as np
import glob
import re
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, Dash
from pathlib import Path

# ===== Functions

def run_dash_app(circles_data_df):
    filename_mask = ""

    # Initialize the Dash app
    app = Dash(__name__)

    # App layout
    app.layout = html.Div([
        html.Label("Enter filename:"),
        dcc.Input(id="filename-input", type="text"),
        dcc.Graph(id='my-graph'),
        html.Img(id="slide_image",src=app.get_asset_url(""), style={'width': '200px'}),
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
    return app

def plot_circles(
        image,
        df
):
    for i, row in df.iterrows():
        cv2.circle(image, row.coordinate, row.radius, (255, 0, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        label = f"{int(row.radius)}"
        cv2.putText(image, label, (row.coordinate[0] - int(row.radius/2), row.coordinate[1] + int(row.radius/2)), font, 1, (0,0,255), 2)
    return image

def read_image(path):
    return cv2.imread(path)

def gray(
        image
):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def blur(
        image,
        intensity,
        type="median"
):
    if type == "median":
        return cv2.medianBlur(image, intensity)
    
def find_circles(
        image,
        method,
        dp,
        minDist,
        param1,
        param2,
        minRadius,
        maxRadius
):
    circles = cv2.HoughCircles(
        image=image, 
        method=method, 
        dp=dp, 
        minDist=minDist,
        param1=param1, 
        param2=param2, 
        minRadius=minRadius, 
        maxRadius=maxRadius
    )
    coordinates = [(x[0],x[1]) for x in np.uint16(np.around(circles))[0, :]]
    radii = [x[2] for x in np.uint16(np.around(circles))[0, :]]
    return pd.DataFrame({
        "coordinate":coordinates,
        "radius":radii
    })

def annotate_images(
        image_paths,
        save_dir,
        blur_intensity=15,
        blur_type="median"
):
    if type(image_paths) == str:
        image_paths = [image_paths]
    circles_data_df = pd.DataFrame()
    for path in image_paths:
        file_name = os.path.basename(path)
        image = read_image(path)
        grayed = gray(image)
        blurred = blur(grayed,blur_intensity,type=blur_type)
        circles_df = find_circles(
            image=blurred,
            method=cv2.HOUGH_GRADIENT, 
            dp=1, 
            minDist=100,
            param1=20, 
            param2=30, 
            minRadius=25, 
            maxRadius=100
        )
        annotated_image = plot_circles(
            image,
            circles_df
        )
        cv2.imwrite(f"{save_dir}/{file_name}", annotated_image)
        circles_df["filename"] = file_name
        circles_data_df = pd.concat([circles_data_df,circles_df])
    circles_data_df.to_csv(f"{save_dir}/1_size_analysis.csv",index=False)
    return circles_data_df

# ===== Pipeline

parser = argparse.ArgumentParser()
parser.add_argument("images_path", help="The path to the directory where images for analysis are stored. This can be either absolute or relative.")
parser.add_argument("save_path", help="The path to the directroy where images which have been annotated should be stored. This can be either absolute or relative.")
args = parser.parse_args()

image_paths = glob.glob(f"{args.images_path}/*/*.jpg") + glob.glob(f"{args.images_path}/*.jpg") + glob.glob(f"{args.images_path}*/*.jpg") + glob.glob(f"{args.images_path}*/*.jpg")
print(f"Found {len(image_paths)} images.")

Path(args.save_path).mkdir(parents=True, exist_ok=True)
circles_data_df = annotate_images(image_paths,args.save_path)
app = run_dash_app(circles_data_df)

if __name__ == "__main__":
    app.run_server(debug=False)