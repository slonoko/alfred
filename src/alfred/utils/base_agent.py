import logging
import os
from llama_index.core import Settings
from alfred.utils.common import (
    configure_logging,
    apply_nest_asyncio,
    load_environment_variables,
    initialize_azure_services,
    initialize_ollama_services,
    read_md_file
)
from alfred.tools.alphavantage_retreaver import AlphaVantageToolSpec
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Context
)
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import FunctionCallingAgent

from llama_index.core.agent.workflow import (
    AgentWorkflow,
    ReActAgent)

class QueryEvent(Event):
    query: str

class FunctionEvent(Event):
    function: str
    documentation: str
    parameters: any

class TraderAgentWorkflow(Workflow):

    @step
    async def start(self, ctx: Context, event: StartEvent) -> QueryEvent:
        self.tool = AlphaVantageToolSpec()
        return QueryEvent(query=event.query)

    @step
    async def find_function(self, ctx: Context, event: QueryEvent) -> FunctionEvent:
        logging.info(f'Query: {event.query}')
        functions =await self.tool.get_relevant_functions(event.query)
        return FunctionEvent(function=functions['function'], documentation=functions['documentation'], parameters=functions['parameters'])

    @step
    async def execute_function(self, ctx: Context, event: FunctionEvent) -> StopEvent:
        res = self.tool.execute_function(event.function, event.parameters)
        print(res)
        return StopEvent(res)
        
        
class BaseAgent:
    def __init__(self, prompt_file, model_name="llama3.1"):
        # Logging configuration
        configure_logging(level=logging.INFO)

        # Apply nest_asyncio
        apply_nest_asyncio()

        # Load environment variables
        load_environment_variables()

        # Initialize services
        self.azure_llm, self.azure_embedding, _ = initialize_azure_services()
        self.ollama_llm, self.ollama_embedding, _ = initialize_ollama_services(model_name)

        Settings.embed_model = self.ollama_embedding
        Settings.llm = self.azure_llm if model_name == 'azure' else self.ollama_llm

        self.prompt = read_md_file(os.path.join(os.getcwd(), prompt_file))

    def prepare_chat(self, tools):
        agent = FunctionCallingAgent.from_tools(
            tools=tools,
            llm=Settings.llm,
        )

        return TraderAgentWorkflow()
