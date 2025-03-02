import pickle
import click
import asyncio
from alfred.tools.flight_assistant import FlightAssistantTool
from alfred.tools.exchange_rate import ExchangeRateTool
from alfred.utils.base_agent import BaseAgent
from alfred.utils.common import save_context, load_context

from llama_index.core.workflow import (
    Context,
    JsonSerializer,
    JsonPickleSerializer,
)

import os

class TravelAssistant(BaseAgent):
    def __init__(self, model_name):
        super().__init__('prompts/flightassistant_prompt.MD', model_name)

    def prepare_chat(self):
        flight_tool = FlightAssistantTool()
        exchange_rate_spec = ExchangeRateTool()
        tools = []
        tools.extend(flight_tool.to_tool_list())
        tools.extend(exchange_rate_spec.to_tool_list())

        return super().prepare_chat(
            agent_name="flightassistant",
            agent_description="Perform flight search and exchange rate conversion",
            tools=tools
        )

async def run_command(question: str = None, memory: bool = False, model_name: str = 'llama3.1'):
    broker = TravelAssistant(model_name)
    workflow = broker.prepare_chat()
    ctx = None
    CTX_PKL = 'ctx_travel_assistant.pkl'

    if memory:
        ctx = load_context(workflow, CTX_PKL)

    handler = workflow.run(ctx=ctx, user_msg=question)
    response = await handler

    if memory:
        save_context(handler, CTX_PKL)

    return str(response)



@click.command()
@click.argument('question')
@click.option('-s', '--store', help='Use memory to store context', type=bool, is_flag=True)
@click.option('-m', '--model', help='The model name', type=str)
def ask(question: str, store: bool, model: str = 'llama3.1'):
    result = asyncio.run(run_command(question, store, model))
    print(result)

if __name__ == "__main__":
    ask()