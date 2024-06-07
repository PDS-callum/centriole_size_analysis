from dash import Dash, dcc, html, Input, Output, State, callback
from utils.general_utils import *
import base64

import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])

def parse_contents(contents, filename, date):
    try:
        if not contents:
            raise Exception("Empty image data uploaded")
        decoded = base64.b64decode(contents)
    except Exception as e:
        print(f"Error decoding image: {e}")
    print(contents[:10])
    try:
        decoded = base64.b64decode(contents)
    except Exception as e:
        print(f"Error decoding base64: {e}")
    # Handle the error case (e.g., return a placeholder message)
    # Read image using OpenCV
    print(type(decoded))
    try:
        image_array = cv2.imdecode(np.fromstring(decoded, np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error decoding image with OpenCV: {e}")
        # Handle the error case (return a placeholder message)
    print(image_array)
    # Convert to grayscale
    gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    # print(gray_image)
    # Encode grayscale image back to base64
    _, buffer = cv2.imencode('.jpg', gray_image)
    grayscale_encoded = base64.b64encode(buffer.tobytes()).decode('utf-8')
    return html.Div("Error decoding image")

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # Update image source with grayscale base64 string
        html.Img(src=f'data:image/jpeg;base64,{grayscale_encoded}'),

        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
        'whiteSpace': 'pre-wrap',
        'wordBreak': 'break-all'
        })
    ])


@callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

if __name__ == '__main__':
    app.run(debug=True)
