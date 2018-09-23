import io
import os
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account
from PIL import Image


# use Google Vision to get labels from each image.
def label(file):
    path = os.getcwd()
    # Please add you json into the folder with all other code files.
    # edit and add your own json file here, replace the "\My First Project-bbdc176f5fe1.json".
    try:
        filename = path + "\My First Project-bbdc176f5fe1.json"
        credentials = service_account.Credentials.from_service_account_file(filename)
        client = vision.ImageAnnotatorClient(credentials=credentials)
    except:
        raise Warning("fail to add the json file")

    with io.open(file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    label_list = []
    for label in labels:
        label_list.append(label.description)
    return label_list



