# Alfred - Personal Assistant

Alfred is a personal assistant designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.

## Prerequisites

- Python 3.10 or higher
- `conda` (Anaconda or Miniconda)
- Docker and Docker Compose
- NVIDIA GPU with CUDA support (recommended)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt) for Docker

## Setup

1. **Clone the repository:**

    ```sh
    git clone git@github.com:slonoko/alfred.git
    cd alfred
    ```

2. **Create a conda environment:**

    ```sh
    conda create --name alfred python=3.10
    conda activate alfred
    ```

3. **Install build dependencies:**

    ```sh
    pip install build setuptools
    ```

4. **Build the package:**

    ```sh
    python -m build
    ```

5. **Set up environment variables:**

    **Create a [`.env`](.env ) file in the [`assistant`](assistant ) directory and add the following variables:**

    ```env
    azure_api_key=<your_azure_api_key>
    azure_endpoint=<your_azure_endpoint>
    azure_api_version=<your_azure_api_version>
    RAPIDAPI_KEY=<rapid_api_key>
    RAPIDAPI_HOST=<host>.p.rapidapi.com
    ```

6. **Install Required Docker Services:**

    a. **Install Ollama:**
    ```sh
    docker run -d --gpus=all --network host \
      -v ollama:/root/.ollama \
      -p 11434:11434 \
      --restart always \
      --name ollama \
      ollama/ollama
    ```

    b. **Install Milvus:**
    ```sh
    # Create Milvus directory
    mkdir .db
    cd .db

    # Download standalone script
    curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh

    # Start Milvus
    bash standalone_embed.sh start
    ```

7. **Install Alfred chat app**

    ```sh
    docker build -t alfred-chat .

    docker run -d -p 8501:8501 --network host \
      --restart always \
      --name alfred \
      alfred-chat
    ```

8. **Optional: Install Open WebUI**

    ```sh
    docker run -d -p 8080:8080 --gpus all --network host \
      -e OLLAMA_BASE_URL=http://localhost:11434 \
      -v <project_path>/alfred/.chat:/app/backend/data \
      --name open-webui \
      --restart always \
      ghcr.io/open-webui/open-webui:cuda
    ```

## Usage

The project provides several commands that can be executed using the CLI:

- **Web app:**

    ```sh
    cd assistant
    streamlit run assistant/chat.py 
    ```

- **Console:**

    ```sh
    cd assistant
    
    # Stock broker
    python stockbroker.py -s -m llama3.1 "what is the current price of nvidia? (in euro)"

    # travel assistant
    python travelassistant.py -s -m llama3.1 "Any direct flights from Stuttgart to Paris in May 2025?"
    ```

## Project Configuration

The project uses [`pyproject.toml`](pyproject.toml ) for configuration. Here are some key sections:

- **Dependencies:**

    ```toml
    [project]
    dependencies = [
        "llama-index-core>=0.10.39.post1",
        "llama-index-readers-file>=0.1.23",
        "llama-index-llms-ollama>=0.1.5",
        "llama-index-embeddings-huggingface>=0.2.0",
        "transformers>=4.41.1",
        "google-api-python-client>=2.130.0",
        "google-auth-httplib2>=0.2.0",
        "google-auth-oauthlib>=1.2.0",
        "beautifulsoup4>=4.12.3",
        "llama-index>=0.10.39",
        "llama-index-vector-stores-chroma>=0.1.5",
        ...
    ]
    ```

- **Scripts:**

    ```toml
    [project.scripts]
    assistant = "assistant.main:cli"
    ```

## License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE ) file for details.

## Authors

- Elie Khoury - [elie.kh@gmail.com](mailto:elie.kh@gmail.com)