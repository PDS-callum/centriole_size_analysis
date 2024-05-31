import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
import plotly.express as px

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

def plot(
        image,
        size=(50,7),
        gray=False
):
    plt.figure(figsize = size)
    if gray:
        plt.imshow(image, interpolation='nearest', cmap="gray")
    else:
        plt.imshow(image, interpolation='nearest')
    plt.show()

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
        cv2.imwrite(save_dir+"/"+file_name, annotated_image)
        circles_df["filename"] = file_name
        circles_data_df = pd.concat([circles_data_df,circles_df])
    return circles_data_df

def get_radii_hist(df,file_name):
    query_df = df.query("file_name == @file_name").copy()
    radii_list = query_df.radii.values[0].split(",")
    fig = px.histogram(radii_list)
    fig.show()