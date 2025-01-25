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
from llama_index.callbacks.aim import AimCallback
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from tools.date_time_retriever import CurrentDateTimeToolSpec
from llama_index.core.agent.workflow import AgentWorkflow
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
MODEL_NAME = "llama3.2:3b-instruct-fp16"

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
    todays_info_spec = CurrentDateTimeToolSpec()
    finances_spec = YahooFinanceToolSpec()

    tools = []
    tools.extend(todays_info_spec.to_tool_list())
    tools.extend(finances_spec.to_tool_list())

    prompt = read_md_file(os.path.join(os.getcwd() ,'assistant/prompts/trader_prompt.MD'))
    agent = AgentWorkflow.from_tools_or_functions (
        tools_or_functions=tools, llm=Settings.llm, system_prompt=prompt)
    
    return agent  

async def run_command():
    agent = prepare_chat()
    command = input(">> Human: ")
    response = await agent.run(command, verbose=True)
    print(f'Agent: {response}')

async def run_command_alt(question:str=None):
    workflow = prepare_chat()
    handler = await workflow.run(user_msg=question)
    print(str(handler)) 
    # async for event in handler.stream_events():
    #     if isinstance(event, AgentStream):
            # print(event.delta, end="", flush=True)
            # print(event.response)  # the current full response
            # print(event.raw)  # the raw llm api response
            # print(event.current_agent_name)  # the current agent name
        # elif isinstance(event, AgentInput):
        #    print(event.input)  # the current input messages
        #    print(event.current_agent_name)  # the current agent name
        # elif isinstance(event, AgentOutput):
        #    print(event.response)  # the current full response
        #    print(event.tool_calls)  # the selected tool calls, if any
        #    print(event.raw)  # the raw llm api response
        # elif isinstance(event, ToolCallResult):
        #    print(event.tool_name)  # the tool name
        #    print(event.tool_kwargs)  # the tool kwargs
        #    print(event.tool_output)  # the tool output
        # elif isinstance(event, ToolCall):
        #     print(event.tool_name)  # the tool name
        #     print(event.tool_kwargs)  # the tool kwargs

@click.command()
@click.argument('question')
def ask(question:str):
    asyncio.run(run_command_alt(question))

if __name__ == "__main__":
    ask()