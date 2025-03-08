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
from llama_index.core.agent.workflow import (
    AgentWorkflow,
    ReActAgent)

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

    def prepare_chat(self, agent_name, agent_description, tools):
        agent = ReActAgent(
            name=agent_name,
            description=agent_description,
            system_prompt=self.prompt,
            tools=tools,
            llm=Settings.llm,
        )

        return AgentWorkflow(agents=[agent], root_agent=agent_name)
