# WasteWise

A web app that detects objects in a live phone camera stream, built as a step towards automatic waste sorting. The browser sends camera frames to a FastAPI backend, which runs object detection and returns bounding boxes and labels; the page draws them over the live video.

**Tech stack:** Python, FastAPI, Ultralytics YOLOv8, JavaScript (camera capture and canvas drawing), Docker, Traefik (TLS termination with Let's Encrypt), Terraform, Azure Container Instances.

University of Geneva project, spring 2024.

## Model

- **First version:** zero-shot detection of waste items with OWLv2, then CLIP to classify each item as organic, plastic, glass, paper or metal waste (Hugging Face `transformers`). See the commit history.
- **Current version:** a faster YOLOv8m detector pretrained on COCO, which recognises everyday objects such as bottles and cups. Detections with confidence above 0.5 are returned.

## Architecture

| Part | What it does |
|------|--------------|
| [frontend/index.html](frontend/index.html) | Captures camera frames in the browser, sends each one to `/classify/` and draws the returned boxes and labels on a canvas |
| [backend/main.py](backend/main.py) | FastAPI app that runs the detector on CPU and serves the frontend |
| [gateway](gateway) | Traefik reverse proxy with automatic Let's Encrypt certificates; browsers allow camera access only over HTTPS |
| [terraform](terraform) | Azure resource group and a container group running the backend and gateway containers side by side |

## Run locally

```bash
docker build -t wastewise .
docker run --rm -p 8080:8080 --entrypoint fastapi wastewise run --host 0.0.0.0 --port 8080
```

Then open [http://localhost:8080](http://localhost:8080) and allow camera access. The `--entrypoint` override makes the server reachable from your machine; the image's default entrypoint listens only inside the Azure container group.

## Deploy to Azure

1. Build the server image from the repository root and the gateway image from [gateway](gateway), and push both to a container registry.
2. In [gateway/dynamic.yml](gateway/dynamic.yml) and [gateway/traefik.yml](gateway/traefik.yml), set your own host name and Let's Encrypt email.
3. Run Terraform with an Azure service principal:

```bash
cd terraform
terraform init
terraform apply \
  -var client_id=... -var client_secret=... -var tenant_id=... -var subscription_id=... \
  -var server_image=<registry>/wastewise -var gateway_image=<registry>/wastewise-gateway
```

Terraform outputs the container group's public host name and IP address.
