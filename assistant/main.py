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
    Settings.llm = Ollama(model="llama3.1", request_timeout=360.0)


def current_date(**kwargs) -> str:
    """
    Get current date
    
    args:
        None
    """
    return f'Current date is {datetime.datetime.now().strftime("%A, %B %d, %Y")}, and time {datetime.datetime.now().strftime("%H:%M:%S")}'


@click.group()
def cli():
    pass


@click.command()
def scan_emails():
    gmail_reader = GmailReader(
        use_iterative_parser=True,max_results=100)
    init_ai()
    # check if storage already exists
    PERSIST_DIR = "./.storage"
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        os.mkdir(".storage")

    emails = gmail_reader.load_data()

    chroma_client = chromadb.PersistentClient(path="./.storage/alfred_db")
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

    chroma_client = chromadb.PersistentClient(path="./.storage/alfred_db")
    chroma_collection = chroma_client.get_collection("alfred")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = index.as_query_engine(llm=Settings.llm)
    email_reader_engine = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="email_reader_engine",
            description="This tool can retrieve email content from google mail inbox"
        )
    )

    agent = ReActAgent.from_tools(
        tools=[todays_info_engine, email_reader_engine], llm=Settings.llm, verbose=True, max_iterations=50)
    agent.reset()

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
