from PIL import Image
import io
import base64
from colormap import rgb2hex

def get_encoded_img(image_path):
    extension = image_path.split('.')[-1]
    try:
        img = Image.open(image_path, mode='r')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
        return f"data:image/{extension};base64,{my_encoded_img}"
    except FileNotFoundError:
        print(f"Image {image_path} not found")
    
def to_hex(color):
    return rgb2hex(*color)

def convert_event_data(event_type, event_data):
    # if event_type == "keydown" or event_type == "keyup":
    #     pass
    # elif event_type == "mousedown" or event_type == "mouseup":
    #     pass
    return event_type, event_data