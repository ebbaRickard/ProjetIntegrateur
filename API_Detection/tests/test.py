import requests
import zipfile
import io
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

filepath="./board.jpg"
file={"file": ("filename", open(filepath, "rb"), "image/jpg")}
r = requests.post("http://localhost:5001/detection",files=file)
r=r.json()

for (data,n) in zip(r["detection"],range(len(r["detection"]))):
    
    numpy_image = np.array(data[f"image{n:04d}"])
    print(np.shape(numpy_image))
    plt.imshow(data[f"image{n:04d}"])
    plt.show()

    PIL_image = Image.fromarray(numpy_image.astype('uint8'), 'RGB')
    PIL_image.show()
"""
    image = Image.new("RGB", (150,150),255)
    data_image = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            data_image[x,y]=(numpy_image[x][y][0],numpy_image[x][y][1],numpy_image[x][y][0])
    image.show()
"""    

