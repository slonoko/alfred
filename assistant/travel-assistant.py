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
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings

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

async def run_command(question:str=None):
    workflow = prepare_chat()
    handler = await workflow.run(user_msg=question)
    print(str(handler)) 
    # async for event in handler.stream_events():
    #     if isinstance(event, AgentStream):
    #         print(event.delta, end="", flush=True)
    #         print(event.response)  # the current full response
    #         print(event.raw)  # the raw llm api response
    #         print(event.current_agent_name)  # the current agent name
    #     elif isinstance(event, AgentInput):
    #        print(event.input)  # the current input messages
    #        print(event.current_agent_name)  # the current agent name
    #     elif isinstance(event, AgentOutput):
    #        print(event.response)  # the current full response
    #        print(event.tool_calls)  # the selected tool calls, if any
    #        print(event.raw)  # the raw llm api response
    #     elif isinstance(event, ToolCallResult):
    #        print(event.tool_name)  # the tool name
    #        print(event.tool_kwargs)  # the tool kwargs
    #        print(event.tool_output)  # the tool output
    #     elif isinstance(event, ToolCall):
    #         print(event.tool_name)  # the tool name
    #         print(event.tool_kwargs)  # the tool kwargs

@click.command()
@click.argument('question')
def ask(question:str):
    asyncio.run(run_command(question))

if __name__ == "__main__":
    ask()