from io import BytesIO
from typing import List

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
from pydantic import BaseModel
from detection import detection
import numpy as np
import os
import zipfile


app = FastAPI()

#for the JSON response
class Prediction(BaseModel):
    filename: str
    content_type: str
    detection: List[dict]=[]


photo_dir="./photos"
zip_dir="photos.zip"


#create a zipfile out of all the photos+send them
def zipfiling(faceup,pathdir=photo_dir,photozip=zip_dir):

    if os.path.exists(pathdir):
            if len(os.listdir(pathdir)) != 0:
                for file in os.listdir(pathdir):
                    os.remove(os.path.join(pathdir,file))
    else:
        os.mkdir(pathdir)

    for (card,i) in zip(faceup,range(0,len(faceup))):
        img=Image.fromarray(np.array(card))
        img.save(f"{pathdir}/{i:04d}.jpeg")


    if os.path.exists(photozip):
        os.remove(photozip)

    zipf=zipfile.ZipFile(photozip,'w', zipfile.ZIP_DEFLATED)
    if len(os.listdir(pathdir)) != 0:
                for file in os.listdir(pathdir):
                    zipf.write(f"{pathdir}/{file}")
                zipf.close()


@app.post("/detection",response_model=Prediction)
async def send_detection(file: UploadFile= File(...)):
     # Ensure that the file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    

    content =await file.read()
    image =Image.open(BytesIO(content))
    
    faceup =  detection(image)
    response=[{f"image{n:04d}":card.tolist()} for (card,n) in zip(faceup,range(len(faceup)))]
 

    return {"filename": file.filename,
        "content_type":file.content_type,
        "detection":response}


if __name__=="__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=5000)