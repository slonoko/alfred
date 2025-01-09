from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.milvus import MilvusVectorStore
import click
import logging
import sys
from llama_index.core.agent import AgentChatResponse
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.tools.code_interpreter import CodeInterpreterToolSpec
from tools.date_time_retriever import CurrentDateTimeToolSpec
from llama_index.core.memory import (
    VectorMemory,
    SimpleComposableMemory,
    ChatMemoryBuffer,
)
import nest_asyncio
from tools.gmail_reader import GmailReader
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core.callbacks import CallbackManager
from llama_index.callbacks.aim import AimCallback
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
import os
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

nest_asyncio.apply()
load_dotenv()

api_key = os.getenv("azure_api_key")
azure_endpoint = os.getenv("azure_endpoint")
api_version = os.getenv("azure_api_version")

azure_llm = AzureOpenAI(
    model="gpt-4o-mini",
    deployment_name="gpt-4o-mini",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

azure_embedding = AzureOpenAIEmbedding(
    model="text-embedding-ada-002", # dim 1536
    deployment_name="text-embedding-ada-002",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

# "nomic-embed-text" as alternative
ollama_embedding = OllamaEmbedding(
    model_name= "bge-m3", # dim 1024
    base_url="http://localhost:11434"
)

ollama_llm = Ollama(model="llama3.1", base_url="http://localhost:11434", request_timeout=360.0)

Settings.embed_model = ollama_embedding
Settings.llm = ollama_llm

aim_callback = AimCallback(repo="/home/elie/projects/alfred/aim")
callback_manager = CallbackManager([aim_callback])

def read_md_file(file_path):
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
    vector_store = MilvusVectorStore(uri="http://localhost:19530", dim=1024, overwrite=True, collection_name="elie_emails")
    history_store = MilvusVectorStore(uri="http://localhost:19530", dim=1024, overwrite=True, collection_name="history")

    gmail_reader = GmailReader(use_iterative_parser=True, max_results=100)
    emails = gmail_reader.load_data()
        
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(
        emails, storage_context=storage_context, embed_model=Settings.embed_model ,show_progress=True, callback_manager=callback_manager
    )


@click.command()
def chat():
    vector_store = MilvusVectorStore(uri="http://localhost:19530", dim=1024, overwrite=False, collection_name="elie_emails")
    history_store = MilvusVectorStore(uri="http://localhost:19530", dim=1024, overwrite=False, collection_name="history")

    vector_memory = VectorMemory.from_defaults(
        vector_store=history_store,  # leave as None to use default in-memory vector store
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

    todays_info_spec = CurrentDateTimeToolSpec()
    finances_spec = YahooFinanceToolSpec()
    code_interpreter_spec = CodeInterpreterToolSpec()

    email_reader_engine = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="elie_khoury_emails_database",
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
