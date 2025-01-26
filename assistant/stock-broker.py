import pickle
import click
import asyncio
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from tools.exchange_rate import ExchangeRateTool
from utils.base_agent import BaseAgent

from llama_index.core.workflow import (
    Context,
    JsonSerializer,
    JsonPickleSerializer,
)

import os

class StockBroker(BaseAgent):
    def __init__(self):
        super().__init__('assistant/prompts/trader_prompt.MD')

    def prepare_chat(self):
        finances_spec = YahooFinanceToolSpec()
        exchange_rate_spec = ExchangeRateTool()
        tools = []
        tools.extend(finances_spec.to_tool_list())
        tools.extend(exchange_rate_spec.to_tool_list())

        return super().prepare_chat(
            agent_name="broker",
            agent_description="Performs stock related operations",
            tools=tools
        )

async def run_command(question: str = None, memory: bool = False):
    broker = StockBroker()
    workflow = broker.prepare_chat()
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