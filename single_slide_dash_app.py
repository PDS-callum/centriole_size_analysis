import dash
from dash import html, dcc, Input, Output
import os
from PIL import Image
import base64

# Define the app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div('Drag and Drop or Browse File'),
        multiple=False
    ),
    html.Img(id='output-image')  # Placeholder for uploaded image
])


@app.callback(
    Output(component_id='output-image', component_property='src'),
    Input(component_id='upload-image', component_property='contents'),
    Input(component_id='upload-image', component_property='filename')
)
def update_image(content, filename):
    if content is not None:
        # Extract image data
        data = content.split(',')[1]
        decoded_data = base64.b64decode(data)

        # Load image using PIL
        with open('temp.jpg', 'wb') as f:
            f.write(decoded_data)
        try:
            pil_image = Image.open('temp.jpg')
            # You can add processing here like resizing, etc.

            # Convert PIL image to encoded format for display
            img_encoded = base64.b64encode(pil_image.tobytes()).decode('ascii')
            return f'data:image/jpeg;base64,{img_encoded}'
        except Exception as e:
            print(f'Error processing image: {e}')
            return dash.no_update  # No update if there's an error

    # Return empty string if no image uploaded
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)
