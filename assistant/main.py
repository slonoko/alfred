from llama_index.core import VectorStoreIndex, Settings, StorageContext, PromptTemplate
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
from llama_index.tools.wikipedia import WikipediaToolSpec
import os
from dotenv import load_dotenv

# Logging configuration
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Apply nest_asyncio
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Configuration Constants
AZURE_LLM_MODEL = "gpt-4o-mini"
AZURE_EMBED_MODEL = "text-embedding-ada-002"
MILVUS_URI = "http://localhost:19530"
OLLAMA_URL = "http://localhost:11434"

# Retrieve environment variables with error handling
api_key = os.getenv("azure_api_key")
azure_endpoint = os.getenv("azure_endpoint")
api_version = os.getenv("azure_api_version")

if not all([api_key, azure_endpoint, api_version]):
    raise EnvironmentError("Missing one or more Azure environment variables")

# Initialize Azure services
azure_llm = AzureOpenAI(
    model=AZURE_LLM_MODEL,
    deployment_name=AZURE_LLM_MODEL,
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

azure_embedding = AzureOpenAIEmbedding(
    model=AZURE_EMBED_MODEL,  # dim 1536
    deployment_name=AZURE_EMBED_MODEL,
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

# "nomic-embed-text" as alternative
ollama_embedding = OllamaEmbedding(
    model_name= "bge-m3", # dim 1024
    base_url=OLLAMA_URL
)

ollama_llm = Ollama(model="llama3.1", base_url=OLLAMA_URL, request_timeout=360.0)

Settings.embed_model = ollama_embedding
Settings.llm = ollama_llm

aim_callback = AimCallback(repo="aim")
callback_manager = CallbackManager([aim_callback])

def read_md_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def prepare_chat():
    vector_store = MilvusVectorStore(uri=MILVUS_URI, dim=1024, overwrite=False, collection_name="elie_emails")
    history_store = MilvusVectorStore(uri=MILVUS_URI, dim=1024, overwrite=False, collection_name="history")

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
    wikipedia_spec = WikipediaToolSpec()

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
    tools.extend(wikipedia_spec.to_tool_list())

    agent = ReActAgent.from_tools(
        tools=tools, llm=Settings.llm, verbose=True, memory=composable_memory, callback_manager=callback_manager, max_iterations=20)
    
    react_system_prompt = PromptTemplate(read_md_file(os.path.join(os.getcwd() ,'assistant/prompts/prompt.sys.MD')))
    #agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})

    return agent  

@click.group()
def cli():
    pass


@click.command()
def scan_emails():
    # https://github.com/run-llama/llama-hub/tree/main/llama_hub/gmail
    # https://pypi.org/project/llama-index-readers-google/
    vector_store = MilvusVectorStore(uri=MILVUS_URI, dim=1024, overwrite=True, collection_name="elie_emails")
    history_store = MilvusVectorStore(uri=MILVUS_URI, dim=1024, overwrite=True, collection_name="history")

    gmail_reader = GmailReader(use_iterative_parser=True, max_results=100)
    emails = gmail_reader.load_data()
        
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    VectorStoreIndex.from_documents(
        emails, storage_context=storage_context, embed_model=Settings.embed_model ,show_progress=True, callback_manager=callback_manager
    )

@click.command()
def chat():
    agent = prepare_chat()
    command = input(">> Human: ")
    while (command != "exit"):
        if (command=="new"):
            agent.reset()
        else:
            response = agent.chat(command)
            print(f'Agent: {response}')
        command = input(">> Human: ")

@click.command()
def chat_inter():
    agent = prepare_chat()
    exit_when_done = True
    task_message = None
    while task_message != "exit":
        task_message = input(">> Human: ")
        if task_message == "exit":
            break

        task = agent.create_task(task_message)

        response = None
        step_output = None
        message = None
        while message != "exit":
            if message is None or message == "":
                step_output = agent.run_step(task.task_id)
            else:
                step_output = agent.run_step(task.task_id, input=message)
            if exit_when_done and step_output.is_last:
                print(
                    ">> Task marked as finished by the agent, executing task execution."
                )
                break

            message = input(
                ">> Add feedback during step? (press enter/leave blank to continue, and type 'exit' to stop): "
            )
            if message == "exit":
                break

        if step_output is None:
            print(">> You haven't run the agent. Task is discarded.")
        elif not step_output.is_last:
            print(">> The agent hasn't finished yet. Task is discarded.")
        else:
            response = agent.finalize_response(task.task_id)
        print(f"Agent: {str(response)}")

cli.add_command(scan_emails)
cli.add_command(chat)
cli.add_command(chat_inter)

if __name__ == "__main__":
    cli()
