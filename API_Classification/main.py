from io import BytesIO
from typing import List

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from ai import load_model,prepare_image,predict
from PIL import Image
from pydantic import BaseModel

app = FastAPI()

model = load_model()

#for the JSON response
class Prediction(BaseModel):
    filename: str
    content_type: str
    predictions: List[dict]=[]

@app.post("/predict",response_model=Prediction)

async def prediction(file: UploadFile = File(...)):
    # Ensure that the file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    content= await file.read()
    image= Image.open(BytesIO(content)).convert("RGB")

    # preprocess the image and prepare it for classification
    image = prepare_image(image, target=(224, 224))
    response = predict(image, model)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "predictions": response,
    }

if __name__=="__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=5000)
