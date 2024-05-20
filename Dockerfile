FROM python:3.12-slim

WORKDIR /root/

COPY backend/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

COPY models/yolov8m.pt .
COPY backend/main.py .
COPY frontend/index.html static/

ENTRYPOINT ["fastapi", "run"]
