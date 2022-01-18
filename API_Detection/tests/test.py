import requests
import zipfile
import io

filepath="./board.jpg"
file={"file": ("filename", open(filepath, "rb"), "image/jpeg")}
r = requests.post("http://0.0.0.0:5000/detection",files=file)
r=r.json()

for image in r["detection"]:
    print("yo")
    

