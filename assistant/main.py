from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import datetime
import click
import logging
import sys
import os
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import AgentChatResponse
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import PromptTemplate
import json;
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.tools.code_interpreter import CodeInterpreterToolSpec
from tools.date_time_retriever import CurrentDateTimeToolSpec, DatetimeToolFnSchema
from llama_index.tools.vector_db.base import VectorDBToolSpec
from llama_index.core.agent import AgentRunner
from llama_index.tools.google import GmailToolSpec
from llama_index.core.memory import (
    VectorMemory,
    SimpleComposableMemory,
    ChatMemoryBuffer,
)
from llama_index.core.llms import ChatMessage
import nest_asyncio
from tools.gmail_reader import GmailReader
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core.callbacks import CallbackManager
from llama_index.callbacks.aim import AimCallback
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from pydantic import BaseModel

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


nest_asyncio.apply()

api_key = "xxx"
azure_endpoint = "https://xxx.openai.azure.com/"
api_version = "2024-05-01-preview"

azure_llm = AzureOpenAI(
    model="gpt-4o-mini",
    deployment_name="gpt-4o-mini",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

# You need to deploy your own embedding model as well as your own chat completion model
azure_embedding = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="text-embedding-ada-002",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

# "nomic-embed-text" as alternative
ollama_embedding = OllamaEmbedding(
    model_name= "bge-m3",
    base_url="http://localhost:11434"
)

ollama_llm = Ollama(model="llama3.1", base_url="http://localhost:11434", request_timeout=360.0)

Settings.embed_model = ollama_embedding
Settings.llm = ollama_llm

chroma_client = chromadb.HttpClient(host="localhost", port=8000)
alfred_collection = chroma_client.get_or_create_collection("alfred")
history_collection = chroma_client.get_or_create_collection("alfred_history")

aim_callback = AimCallback(repo="/home/elie/Projects/alfred/aim")
callback_manager = CallbackManager([aim_callback])

def read_md_file(file_path):
    """
    Reads an MD file and returns its content.

    Args:
        file_path (str): The path to the MD file.

    Returns:
        str: The content of the MD file.
    """

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    

@click.group()
def cli():
    pass


@click.command()
def scan_emails():
    # https://github.com/run-llama/llama-hub/tree/main/llama_hub/gmail
    # https://pypi.org/project/llama-index-readers-google/
    gmail_reader = GmailReader(use_iterative_parser=True)
    emails = gmail_reader.load_data()
        
    vector_store = ChromaVectorStore(chroma_collection=alfred_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(
        emails, storage_context=storage_context, embed_model=Settings.embed_model ,show_progress=True, use_async=True
    )


@click.command()
def chat():
    vector_store = ChromaVectorStore(chroma_collection=alfred_collection)
    history_store = ChromaVectorStore(chroma_collection=history_collection)

    vector_memory = VectorMemory.from_defaults(
        vector_store=None,  # leave as None to use default in-memory vector store
        embed_model=Settings.embed_model,
        retriever_kwargs={"similarity_top_k": 1},
    )   
    chat_memory_buffer = ChatMemoryBuffer.from_defaults()

    composable_memory = SimpleComposableMemory.from_defaults(
        primary_memory=chat_memory_buffer,
        secondary_memory_sources=[vector_memory],
    )

    index = VectorStoreIndex.from_vector_store(vector_store, callback_manager=callback_manager)
    query_engine = index.as_query_engine(llm=Settings.llm, similarity_top_k=1)

    # gmail_spec = GmailToolSpec()
    todays_info_spec = CurrentDateTimeToolSpec()
    finances_spec = YahooFinanceToolSpec()
    code_interpreter_spec = CodeInterpreterToolSpec()

    email_reader_engine = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="emails_database_retriever",
            description="A useful tool that accesses a database containing all emails of Elie Khoury. If the user asks about Elie Khoury, look in here first"
        )
    )

    tools = [email_reader_engine]
    tools.extend(todays_info_spec.to_tool_list())
    tools.extend(finances_spec.to_tool_list())
    tools.extend(code_interpreter_spec.to_tool_list())

    agent = ReActAgent.from_tools(
        tools=tools, llm=Settings.llm, verbose=True, memory=composable_memory, callback_manager=callback_manager)

    #react_system_prompt = PromptTemplate(read_md_file(os.path.join(os.getcwd() ,'assistant/prompt.sys.MD')))
    #agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})

    command = input("Q: ")
    while (command != "exit"):
        if (command=="new"):
            agent.reset()
        else:
            response:AgentChatResponse = agent.chat(command)
            print(response)
        command = input("Q: ")


cli.add_command(scan_emails)
cli.add_command(chat)

if __name__ == "__main__":
    cli()
