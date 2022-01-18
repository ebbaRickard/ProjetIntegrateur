import requests

filepath="./tests/files/picture.jpg"
files={"file": ("filename", open(filepath, "rb"), "image/jpeg")}
r = requests.post("http://0.0.0.0:5000/predict",files=files)
print(r.json())

