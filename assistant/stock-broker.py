import pickle
import click
import logging
import sys
import os
import nest_asyncio
import asyncio
from dotenv import load_dotenv
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
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
from assistant.utils.common import (
    configure_logging,
    apply_nest_asyncio,
    load_environment_variables,
    initialize_azure_services,
    initialize_ollama_services,
    read_md_file
)

from llama_index.core.workflow import (
    Context,
    JsonSerializer,
    JsonPickleSerializer,
)

# Logging configuration
configure_logging()

# Apply nest_asyncio
apply_nest_asyncio()

# Load environment variables
load_environment_variables()

# Initialize services
azure_llm, azure_embedding, _ = initialize_azure_services()
ollama_llm, ollama_embedding, _ = initialize_ollama_services()

Settings.embed_model = ollama_embedding
Settings.llm = azure_llm

def prepare_chat():
    finances_spec = YahooFinanceToolSpec()
    exchange_rate_spec = ExchangeRateTool()
    tools = []
    tools.extend(finances_spec.to_tool_list())
    tools.extend(exchange_rate_spec.to_tool_list())

    prompt = read_md_file(os.path.join(os.getcwd(), 'assistant/prompts/trader_prompt.MD'))

    broker_agent = ReActAgent(
        name="broker",
        description="Performs stock related operations",
        system_prompt=prompt,
        tools=tools,
        llm=Settings.llm,
    )

    agent = AgentWorkflow(agents=[broker_agent], root_agent="broker")
    
    return agent  

async def run_command(question: str = None, memory: bool = False):
    workflow = prepare_chat()
    ctx = None
    CTX_PKL = 'ctx_stock_broker.pkl'

    if memory and os.path.exists(CTX_PKL):
        with open(CTX_PKL, 'rb') as f:
            ctx_dict = pickle.load(f)
            ctx = Context.from_dict(workflow, data=ctx_dict, serializer=JsonSerializer())

    handler = workflow.run(ctx=ctx, user_msg=question)
    response = await handler

    if memory:
        ctx_dict = handler.ctx.to_dict(serializer=JsonPickleSerializer())
        with open(CTX_PKL, 'wb') as f:
            pickle.dump(ctx_dict, f)

    print(str(response)) 

@click.command()
@click.argument('question')
@click.option('-m', '--memory', help='Use memory to store context', type=bool, is_flag=True)
def ask(question: str, memory: bool):
    asyncio.run(run_command(question, memory))

if __name__ == "__main__":
    ask()