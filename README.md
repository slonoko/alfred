# Alfred - Personal Assistant

Alfred is a personal assistant designed to help with a variety of tasks, from answering questions to providing summaries to other types of analyses.

## Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)
- `virtualenv` (optional but recommended)

## Setup

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a [.env](http://_vscodecontentref_/9) file in the root directory and add the following variables:

    ```env
    azure_api_key=<your_azure_api_key>
    azure_endpoint=<your_azure_endpoint>
    azure_api_version=<your_azure_api_version>
    ```

5. **Run the application:**

    ```sh
    python assistant/main.py
    ```

## Usage

The project provides several commands that can be executed using the CLI:

- **Scan Emails:**

    ```sh
    python assistant/main.py scan_emails
    ```

- **Chat:**

    ```sh
    python assistant/main.py chat
    ```

## Project Configuration

The project uses [pyproject.toml](http://_vscodecontentref_/10) for configuration. Here are some key sections:

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

This project is licensed under the MIT License. See the [LICENSE](http://_vscodecontentref_/11) file for details.

## Authors

- Elie Khoury - [elie.kh@gmail.com](mailto:elie.kh@gmail.com)