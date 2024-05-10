import io
from typing import Annotated

from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from transformers import pipeline

app = FastAPI()
models = {}
object_labels = [
    "Face",
]
class_labels = [
    "Male",
    "Female",
]


@app.on_event("startup")
def startup_event():
    models["classifier"] = pipeline("zero-shot-image-classification", "openai/clip-vit-base-patch16")
    models["detector"] = pipeline("zero-shot-object-detection", "google/owlv2-base-patch16-ensemble")


@app.post("/classify/")
async def classify(data: Annotated[bytes, Body()]):
    response = []
    image = Image.open(io.BytesIO(data))
    objects = models["detector"](image, candidate_labels=object_labels)
    for object in objects:
        box = object["box"]
        rect = image.crop([box["xmin"], box["ymin"], box["xmax"], box["ymax"]])
        classes = models["classifier"](rect, candidate_labels=class_labels)
        response.append({
            "rect": [
                box["xmin"],
                box["ymin"],
                box["xmax"] - box["xmin"],
                box["ymax"] - box["ymin"],
            ],
            "label": max(classes, key=lambda x: x["score"])["label"],
        })
    return JSONResponse(response)


app.mount("/", StaticFiles(directory="static", html=True))
