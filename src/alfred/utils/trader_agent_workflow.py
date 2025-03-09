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
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Context
)
import json

from alfred.utils.alphavantage import AlphaVantageUtils

configure_logging(level=logging.INFO)
load_environment_variables()

class StepsEvent(Event):
    pass

class QueryEvent(Event):
    query: str

class FunctionEvent(Event):
    function: str
    documentation: str
    parameters: dict

class TraderAgentWorkflow(Workflow):

    def __init__(self, model_name):
        self.model_name = model_name
        super().__init__(timeout=300, num_concurrent_runs=10, verbose=True)

    @step
    async def start(self, ctx: Context, event: StartEvent) -> StepsEvent:
        # Initialize services
        self.azure_llm, self.azure_embedding, _ = initialize_azure_services()
        self.ollama_llm, self.ollama_embedding, _ = initialize_ollama_services(self.model_name)

        Settings.embed_model = self.ollama_embedding
        Settings.llm = self.azure_llm if self.model_name == 'azure' else self.ollama_llm

        self.tool = AlphaVantageUtils()

        raw_json = Settings.llm.complete(
            f"""
            You are a professional trading broker.
            You have been asked the following question.

            <question>
            {event.query}
            </question>
            
            reply to the question in the form of a list of steps to be taken to answer the question (specify if a step depends on another).
            Convert it into a JSON object containing only the list, in the form {{ steps: [{{"id":1,"action":"", "description":"", "depends_on":1}}] }}.
            Return JSON ONLY, no markdown.
            """)
        steps = json.loads(raw_json.text)
        logging.info(raw_json)

        await ctx.set("steps", steps["steps"])
        return StepsEvent()
    
    @step
    async def steps_function(self, ctx: Context, event: StepsEvent) -> QueryEvent:
        steps = await ctx.get("steps")
        for step in steps:
            if step['depends_on'] == None:
                logging.info(f"Running Step {step['id']}: {step['action']}")
                ctx.send_event(QueryEvent(query=step['action']))

        return 

    @step
    async def find_function(self, ctx: Context, event: QueryEvent) -> FunctionEvent:
        logging.info(f'Query: {event.query}')
        functions =await self.tool.get_relevant_functions(event.query)
        return FunctionEvent(function=functions['function'], documentation=functions['documentation'], parameters=functions['parameters'])

    @step
    async def execute_function(self, ctx: Context, event: FunctionEvent) -> StopEvent:
        res = self.tool.execute_function(event.function, event.parameters)
        logging.info(res)
        return StopEvent(res)
        