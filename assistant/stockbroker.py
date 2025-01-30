import click
import asyncio
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from tools.financial_data import FinancialDataToolSpec
from tools.exchange_rate import ExchangeRateTool
from utils.base_agent import BaseAgent
from utils.common import save_context, load_context

# python assistant/stock-broker.py -m "considering the drop in stock price of nvidia this week, do you still recommend buying nvidia shares? explain your analyis, and provide me in the end with a concrete recommendation"

class StockBroker(BaseAgent):
    def __init__(self, model_name):
        super().__init__('assistant/prompts/trader_prompt.MD', model_name=model_name)

    def prepare_chat(self):
        finances_spec = FinancialDataToolSpec()
        exchange_rate_spec = ExchangeRateTool()
        tools = []
        tools.extend(finances_spec.to_tool_list())
        tools.extend(exchange_rate_spec.to_tool_list())

        return super().prepare_chat(
            agent_name="broker",
            agent_description="Performs stock related operations",
            tools=tools
        )

async def run_command(question: str = None, memory: bool = False, model_name: str = 'llama3.1'):
    broker = StockBroker(model_name)
    workflow = broker.prepare_chat()
    ctx = None
    CTX_PKL = 'ctx_stock_broker.pkl'

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