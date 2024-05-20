import io
from typing import Annotated

from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from ultralytics import YOLO

app = FastAPI()
models = {}


@app.on_event("startup")
def startup_event():
    models["detector"] = YOLO("yolov8m.pt")


@app.post("/classify/")
async def classify(data: Annotated[bytes, Body()]):
    response = []
    pred = models["detector"].predict(Image.open(io.BytesIO(data)))[0]
    boxes = pred.boxes
    for conf, xyxy, cls in zip(boxes.conf, boxes.xyxy, boxes.cls):
        if conf.item() > 0.5:
            response.append({
                "rect": xyxy.tolist(),
                "label": pred.names[cls.item()],
            })
    return JSONResponse(response)


app.mount("/", StaticFiles(directory="static", html=True))
