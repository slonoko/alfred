# Alfred - Personal Assistant

Alfred is a personal assistant designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/)
- Docker and Docker Compose
- NVIDIA GPU with CUDA support (recommended)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-apt) for Docker

## Setup

1. **Clone the repository:**

    ```sh
    git clone git@github.com:slonoko/alfred.git
    cd alfred
    ```

2. **Initialize a poetry environment:**

    ```sh
    cd alfred
    poetry init
    poetry install
    ```

3. **Install build dependencies:**

    ```sh
    poetry install
    ```

4. **Set up environment variables:**

    **Create a [`.env`](.env ) file in the [`src/alfred`](Alfred) directory and add the following variables:**

    ```env
    azure_api_key=<your_azure_api_key>
    azure_endpoint=<your_azure_endpoint>
    azure_api_version=<your_azure_api_version>
    RAPIDAPI_KEY=<key>
    SKYSCANNER_HOST=<subdomain>.p.rapidapi.com
    INVESTING_HOST=<subdomain>.p.rapidapi.com
    ALPHA_VANTAGE_KEY=<av_key>
    ALPHA_VANTAGE_URL=<full url>
    ollama_server=<server_url>
    fcts_path=<full path of the json file>
    ```

5. **Install Required Docker Services:**

    a. **Install Ollama:**
    ```sh
    docker run -d --gpus=all --network host \
      -v ollama:/root/.ollama \
      -p 11434:11434 \
      --restart always \
      --name ollama \
      ollama/ollama
    ```
    b. **Install Alfred chat app**

    ```sh
    docker build -t alfred-chat .

    docker run -d -p 8501:8501 --network host \
      --restart always \
      --name alfred \
      alfred-chat
    ```

6. **Install Optional Docker Services:**
    a. **Optional: Install Milvus:**
    ```sh
    # Create Milvus directory
    mkdir .db
    cd .db

    # Download standalone script
    curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh

    # Start Milvus
    bash standalone_embed.sh start
    ```

    b. **Optional: Install Open WebUI**

    ```sh
    docker run -d -p 8080:8080 --gpus all --network host \
      -e OLLAMA_BASE_URL=http://localhost:11434 \
      -v <project_path>/alfred/.chat:/app/backend/data \
      --name open-webui \
      --restart always \
      ghcr.io/open-webui/open-webui:cuda
    ```
    
    c. **Optional: Install Chroma:**
    ```sh
    docker run -d -p 8000:8000 --network host --name chromadb -v ~/.storage/alfred_db/:/chroma/chroma --restart always chromadb/chroma
    ```

## Usage

The project provides several commands that can be executed using the CLI:

- **Web app:**

    ```sh
    cd assistant
    streamlit run chat.py 
    ```

- **Console:**

    ```sh
    cd src/alfred
    
    # Stock broker
    python stockbroker.py -s -m llama3.1 "what is the current price of nvidia? (in euro)"

    # travel assistant
    python travelassistant.py -s -m llama3.1 "Any direct flights from Stuttgart to Paris in May 2025?"
    ```

## License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE ) file for details.

## Authors

- Elie Khoury - [elie.kh@gmail.com](mailto:elie.kh@gmail.com)