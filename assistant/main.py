from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from gmail import GmailReader
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
import prompt_template;
import json;
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.tools.code_interpreter import CodeInterpreterToolSpec

logging.basicConfig(stream=sys.stdout, level=logging.WARN)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


api_key = "xxx"
azure_endpoint = "https://xxx.openai.azure.com/"
api_version = "2024-05-01-preview"

llm = AzureOpenAI(
    model="gpt-4o-mini",
    deployment_name="gpt-4o-mini",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

# You need to deploy your own embedding model as well as your own chat completion model
embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="text-embedding-ada-002",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

ollama_embedding = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url="http://localhost:11434"
)


def init_ai():
    Settings.embed_model = ollama_embedding # HuggingFaceEmbedding(model_name="BAAI/bge-m3")  # https://huggingface.co/BAAI/bge-m3

    # ollama
    # https://github.com/ollama/ollama
    Settings.llm = Ollama(model="llama3.2", base_url="http://localhost:11434", request_timeout=360.0)

def current_date(**kwargs) -> str:
    """
    This function returns the current date and time in a JSON format
    """
    current_datetime = datetime.datetime.now()
    output = {"date": current_datetime.strftime("%A, %B %d, %Y"),"time": current_datetime.strftime("%H:%M:%S")} 
    return json.dumps(output)


@click.group()
def cli():
    pass


@click.command()
def scan_emails():
    gmail_reader = GmailReader(
        use_iterative_parser=True)
    init_ai()
    emails = gmail_reader.load_data()

    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    
    chroma_collection = chroma_client.get_or_create_collection("alfred")
        
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(
        emails, storage_context=storage_context, embed_model=Settings.embed_model ,show_progress=True, use_async=True
    )


@click.command()
def chat():
    init_ai()

    todays_info_engine = FunctionTool.from_defaults(
        fn=current_date,
        name="todays_info_engine",
        description="This tool provides information about the current date and time"
    )

    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    chroma_collection = chroma_client.get_collection("alfred")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = index.as_query_engine(llm=Settings.llm)
    email_reader_engine = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="email_reader_engine",
            description="Primary tool to search through emails for information and answer questions. "
        )
    )

    code_spec = CodeInterpreterToolSpec()

    tools = []
    tools.append(todays_info_engine)
    tools.append(email_reader_engine)
    tools.append(code_spec.to_tool_list()[0])
    agent = ReActAgent.from_tools(
        tools=tools, llm=Settings.llm, verbose=True, max_iterations=25)

    #react_system_prompt = PromptTemplate(prompt_template.react_system_header_str)
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
