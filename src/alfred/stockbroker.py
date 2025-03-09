import click
import asyncio
from alfred.tools.alphavantage_retreaver import AlphaVantageToolSpec
from alfred.tools.exchange_rate import ExchangeRateTool
from alfred.utils.base_agent import BaseAgent
from alfred.utils.common import save_context, load_context
from alfred.utils.trader_agent_workflow import TraderAgentWorkflow
# python assistant/stock-broker.py -m "considering the drop in stock price of nvidia this week, do you still recommend buying nvidia shares? explain your analyis, and provide me in the end with a concrete recommendation"
# python stockbroker.py -s -m llama3.1 "what is the current stock price of NVIDIA?"

async def run_command(
    question: str = None, memory: bool = False, model_name: str = "llama3.1"
):
    workflow = TraderAgentWorkflow(model_name)
    ctx = None
    CTX_PKL = "ctx_stock_broker.pkl"

    if memory:
        ctx = load_context(workflow, CTX_PKL)

    handler = workflow.run(ctx=ctx, query=question)
    response = await handler

    if memory:
        save_context(handler, CTX_PKL)

    return str(response)


@click.command()
@click.argument("question")
@click.option(
    "-s", "--store", help="Use memory to store context", type=bool, is_flag=True
)
@click.option("-m", "--model", help="The model name", type=str)
def ask(question: str, store: bool, model: str = "llama3.1"):
    result = asyncio.run(run_command(question, store, model))
    print(result)


if __name__ == "__main__":
    ask()
