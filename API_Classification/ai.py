import warnings

import random


from PIL import Image

import numpy as np

from tensorflow.keras.applications import (
    vgg16,
    resnet50,
    mobilenet,
    inception_v3
)



from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from os import listdir, walk
from os.path import isfile, join


def load_model():
    #loads and returns model
    model = vgg16.VGG16(weights='imagenet')
    print("Model is loaded")
    return model


def prepare_image(img,target):
    #turning image into array 
    image = img.resize(target)
    image=img_to_array(img.resize(target))
    image = np.expand_dims(image, axis=0)
    image = vgg16.preprocess_input(image.copy())

    return image


def predict(image,model):
    preds=decode_predictions(model.predict(image))[0]
    response = [
        {"class": pred[1], "score": float(round(pred[2], 3))} for pred in preds
    ]
    return response


'''
#init the models
vgg_model = vgg16.VGG16(weights='imagenet')
 inception_model = inception_v3.InceptionV3(weights='imagenet')
 resnet_model = resnet50.ResNet50(weights='imagenet')
 mobilenet_model = mobilenet.MobileNet(weights='imagenet')

path_dir = "imageNet"

labels_name = []
data = []
labels = []

dirs = [d for d in walk(path_dir)] # list all file in given directory
i_label = 0
for d in dirs[0][1]:
    labels_name.append(d)
    files = [f for f in listdir(f'{path_dir}/{d}') if isfile(join(f'{path_dir}/{d}', f))] # list all file in given directory

    for f in files:
        original = load_img(f'{path_dir}/{d}/{f}', target_size=(224, 224))  # Extract image data
        data.append(img_to_array(original))
        # Add data and label to X and labels
        labels.append(i_label)
    i_label += 1


# Guessing and printing random image
index = random.randint(0,np.shape(labels)[0])
image_batch = np.expand_dims(data[index], axis=0)
processed_image = vgg16.preprocess_input(image_batch.copy())
predictions = vgg_model.predict(processed_image)

label_vgg = decode_predictions(predictions)

# print VGG16 predictions
for prediction_id in range(len(label_vgg[0])):
    print(label_vgg[0][prediction_id][1])


print("This is a {}".format(labels_name[labels[index]]))
'''
