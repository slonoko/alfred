import os
import logging
import sys
import nest_asyncio
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import Settings
from llama_index.core.workflow import (
    Context,
    JsonSerializer,
    JsonPickleSerializer,
)
import pickle


# Logging configuration
def configure_logging(level=logging.INFO):
    logging.basicConfig(stream=sys.stdout, level=level)


# Apply nest_asyncio
def apply_nest_asyncio():
    nest_asyncio.apply()


# Load environment variables
def load_environment_variables():
    load_dotenv()


# Initialize Azure services
def initialize_azure_services():
    AZURE_LLM_MODEL = "gpt-4o-mini"
    AZURE_EMBED_MODEL = "text-embedding-ada-002"
    api_key = os.getenv("azure_api_key")
    azure_endpoint = os.getenv("azure_endpoint")
    api_version = os.getenv("azure_api_version")

    if not all([api_key, azure_endpoint, api_version]):
        raise EnvironmentError("Missing one or more Azure environment variables")

    azure_llm = AzureOpenAI(
        model=AZURE_LLM_MODEL,
        deployment_name=AZURE_LLM_MODEL,
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )

    azure_embedding = AzureOpenAIEmbedding(
        model=AZURE_EMBED_MODEL,
        deployment_name=AZURE_EMBED_MODEL,
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )

    return azure_llm, azure_embedding, 1536


# Initialize Ollama services
def initialize_ollama_services(model_name):
    OLLAMA_URL = "http://localhost:11434"
    MODEL_NAME = "llama3.1" if model_name == 'azure' else model_name # deepseek-r1:8b, llama3.1, olmo2, mistral, dolphin3
    EMBED_MODEL_NAME = "bge-m3"

    ollama_embedding = OllamaEmbedding(
        model_name=EMBED_MODEL_NAME, base_url=OLLAMA_URL  # dim 1024
    )

    ollama_llm = Ollama(model=MODEL_NAME, base_url=OLLAMA_URL, request_timeout=360.0)

    return ollama_llm, ollama_embedding, 1024


# Read markdown file
def read_md_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


def save_context(handler, pkl_file):
    ctx_dict = handler.ctx.to_dict(serializer=JsonPickleSerializer())
    with open(pkl_file, "wb") as f:
        pickle.dump(ctx_dict, f)


def load_context(workflow, pkl_file):
    ctx = None

    if os.path.exists(pkl_file):
        with open(pkl_file, "rb") as f:
            ctx_dict = pickle.load(f)
            ctx = Context.from_dict(
                workflow, data=ctx_dict, serializer=JsonSerializer()
            )
    return ctx
