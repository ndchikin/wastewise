FROM python:3.12-slim

WORKDIR /root/

RUN pip install huggingface-hub==0.23.0
RUN huggingface-cli download openai/clip-vit-base-patch16 --include *.json *.txt *.bin
RUN huggingface-cli download google/owlv2-base-patch16-ensemble --include *.json *.txt *.safetensors

COPY backend/requirements.txt .
RUN pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

COPY backend/main.py .
COPY frontend/index.html static/

ENTRYPOINT ["fastapi", "run"]
