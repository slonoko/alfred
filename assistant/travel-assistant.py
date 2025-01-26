import json
import pickle
import click
import logging
import sys
import os
import nest_asyncio
import asyncio
from dotenv import load_dotenv
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core.callbacks import CallbackManager
from tools.flight_assistant import FlightAssistantTool
from tools.exchange_rate import ExchangeRateTool
from llama_index.core.agent.workflow import (
    AgentWorkflow,
    ReActAgent,
    FunctionAgent,
    AgentStream,
    AgentInput,
    AgentOutput,
    ToolCall,
    ToolCallResult
)
from llama_index.core.workflow import (
    Context,
    JsonSerializer,
    JsonPickleSerializer,
)
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings

# Logging configuration
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
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
MODEL_NAME = "llama3.1"

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

ollama_llm = Ollama(model=MODEL_NAME, base_url=OLLAMA_URL, request_timeout=360.0)

Settings.embed_model = ollama_embedding
Settings.llm = azure_llm

def read_md_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def prepare_chat():
    flight_tool = FlightAssistantTool()
    exchange_rate_spec = ExchangeRateTool()
    tools = []
    tools.extend(flight_tool.to_tool_list())
    tools.extend(exchange_rate_spec.to_tool_list())

    prompt = read_md_file(os.path.join(os.getcwd() ,'assistant/prompts/flightassistant_prompt.MD'))

    broker_agent = ReActAgent(
        name="flightassistant",
        description="Perform flight search and exchange rate conversion",
        system_prompt=prompt,
        tools=tools,
        llm=Settings.llm,
    )

    agent = AgentWorkflow(agents=[broker_agent], root_agent="flightassistant")
    
    return agent  

async def run_command(question:str=None, memory:bool=True):
    workflow = prepare_chat()
    ctx = None

    if memory and os.path.exists('context_dict.pkl'):
        with open('context_dict.pkl', 'rb') as f:
            ctx_dict = pickle.load(f)
            ctx = Context.from_dict(workflow, data=ctx_dict, serializer=JsonSerializer())

    handler = workflow.run(ctx=ctx, user_msg=question)
    response = await handler

    if memory:
        ctx_dict = handler.ctx.to_dict(serializer=JsonPickleSerializer())
        with open('context_dict.pkl', 'wb') as f:
            pickle.dump(ctx_dict, f)

    print(str(response)) 
    
@click.command()
@click.argument('question')
@click.option('-m', '--memory', help='Use memory to store context', type=bool, is_flag=True) # prompt=True https://click.palletsprojects.com/en/stable/options/
def ask(question:str, memory:bool):
    asyncio.run(run_command(question, memory))

if __name__ == "__main__":
    ask()