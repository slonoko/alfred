# alfred
Alfred - Personal butler
start ollama: ollama serve
chroma run --path ./.storage/alfred_db --host 0.0.0.0

docker network create -d bridge smartnet
docker run -d --gpus=all --network host -v ollama:/root/.ollama -p 11434:11434  --restart always --name ollama ollama/ollama
docker run -d -p 8000:8000 --network host --name chromadb -v /home/elie/Projects/alfred/.storage/alfred_db/:/chroma/chroma  --restart always chromadb/chroma
docker run -d -p 9099:9099  --network host -e PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python -v /home/elie/Projects/alfred/pipelines:/app/pipelines --name pipelines --restart always ghcr.io/open-webui/pipelines:main

docker run -d -p 8080:8080  --gpus all --network host -e OLLAMA_BASE_URL=http://localhost:11434 -v /home/elie/Projects/alfred/.chat:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda

docker run -d -p 43800:43800 --network host -v /home/elie/Projects/alfred/.aim:/opt/aim  --restart always aimstack/aim
