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
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.tools.google import GmailToolSpec
from llama_index.tools.wikipedia import WikipediaToolSpec
from llama_index.core import PromptTemplate
import prompt_template;
import json;

# tool_spec = GmailToolSpec()
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

#https://github.com/run-llama/llama-agents

def init_ai():
    # bge-base embedding model
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-m3")  # https://huggingface.co/BAAI/bge-m3
    # Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    # ollama
    # https://github.com/ollama/ollama
    Settings.llm = Ollama(model="llama3.2:3b", request_timeout=360.0)

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
    chroma_collection = chroma_client.create_collection("alfred")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(
        emails, storage_context=storage_context, show_progress=True, use_async=True
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

    tool_spec = WikipediaToolSpec()
    tools = []
    tools.append(todays_info_engine)
    tools.append(email_reader_engine)
    agent = ReActAgent.from_tools(
        tools=tools, llm=Settings.llm, verbose=True, max_iterations=25)

    react_system_prompt = PromptTemplate(prompt_template.react_system_header_str)

    #agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})

    command = input("Q: ")
    while (command != "exit"):
        if (command=="new"):
            agent.reset()
        else:
            print(
                agent.chat(
                    command
                )
            )
        command = input("Q: ")


cli.add_command(scan_emails)
cli.add_command(chat)

if __name__ == "__main__":
    cli()
