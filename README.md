# Alfred - Personal Assistant

Alfred is a personal assistant designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.

## Prerequisites

- Python 3.10 or higher
- `conda` (Anaconda or Miniconda)
- Docker (for optional services)

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

5. **Install the built package:**

    ```sh
    pip install dist/*.whl
    ```

6. **Set up environment variables:**

    Create a [`.env`](.env ) file in the root directory and add the following variables:

    ```env
    azure_api_key=<your_azure_api_key>
    azure_endpoint=<your_azure_endpoint>
    azure_api_version=<your_azure_api_version>
    ```

7. **Optional: Install Chroma**

    ```sh
    docker run -d -p 8000:8000 --network host --name chromadb \
      -v <project_path>/alfred/.storage/alfred_db/:/chroma/chroma \
      --restart always chromadb/chroma
    ```

8. **Optional: Install Open WebUI**

    ```sh
    docker run -d -p 8080:8080 --gpus all --network host \
      -e OLLAMA_BASE_URL=http://localhost:11434 \
      -v <project_path>/alfred/.chat:/app/backend/data \
      --name open-webui --restart always \
      ghcr.io/open-webui/open-webui:cuda
    ```

## Usage

The project provides several commands that can be executed using the CLI:

- **Scan Emails:**

    ```sh
    python assistant/main.py scan-emails
    ```

- **Chat:**

    ```sh
    python assistant/main.py chat
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