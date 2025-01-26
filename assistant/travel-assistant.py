import pickle
import click
import asyncio
from tools.flight_assistant import FlightAssistantTool
from tools.exchange_rate import ExchangeRateTool
from utils.base_agent import BaseAgent

from llama_index.core.workflow import (
    Context,
    JsonSerializer,
    JsonPickleSerializer,
)

import os

class TravelAssistant(BaseAgent):
    def __init__(self):
        super().__init__('assistant/prompts/flightassistant_prompt.MD')

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

async def run_command(question: str = None, memory: bool = True):
    assistant = TravelAssistant()
    workflow = assistant.prepare_chat()
    ctx = None
    CTX_PKL = 'ctx_travel_assistant.pkl'

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