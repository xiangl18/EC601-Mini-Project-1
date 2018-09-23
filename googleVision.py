import io
import os
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image

# use Google Vision to get labels from each image.
def label(file):
    client = vision.ImageAnnotatorClient()
    with io.open(file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    label_list = []
    for label in labels:
        label_list.append(label.description)
    return label_list



