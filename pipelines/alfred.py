"""
title: Alfred Pipeline
author: Elie Khoury
date: 2024-10-23
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from a knowledge base using the Llama Index library.
requirements: llama-index,chromadb,llama-index-vector-stores-chroma,llama-index-core,llama-index-llms-ollama,llama-index-embeddings-huggingface,llama-index-embeddings-ollama, llama-index-tools-code-interpreter
"""

from typing import List, Union, Generator, Iterator
import datetime
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.tools import QueryEngineTool, ToolMetadata
import logging
from llama_index.core.base.response.schema import Response, StreamingResponse
from llama_index.embeddings.ollama import OllamaEmbedding
from pydantic import BaseModel
import os
from llama_index.tools.code_interpreter import CodeInterpreterToolSpec

class Pipeline:

    class Valves(BaseModel):
        LLAMAINDEX_OLLAMA_BASE_URL: str
        LLAMAINDEX_MODEL_NAME: str
        LLAMAINDEX_EMBEDDING_MODEL_NAME: str
        CHROMA_HOST: str
        CHROMA_PORT: int

    def __init__(self):
        self.documents = None
        self.index = None
        self.agent = None
        self.valves = self.Valves(
            **{
                "LLAMAINDEX_OLLAMA_BASE_URL": os.getenv("LLAMAINDEX_OLLAMA_BASE_URL", "http://localhost:11434"),
                "LLAMAINDEX_MODEL_NAME": os.getenv("LLAMAINDEX_MODEL_NAME", "llama3.2:1b"),
                "LLAMAINDEX_EMBEDDING_MODEL_NAME": os.getenv("LLAMAINDEX_EMBEDDING_MODEL_NAME", "bge-m3"),
                "CHROMA_HOST": os.getenv("CHROMA_HOST", "localhost"),
                "CHROMA_PORT": int(os.getenv("CHROMA_PORT", 8000)),
            }
        )

    def current_date(self, **kwargs) -> str:
        return f'Current date is {datetime.datetime.now().strftime("%A, %B %d, %Y")}, and time {datetime.datetime.now().strftime("%H:%M:%S")}'

    async def on_startup(self):
        # This function is called when the server is started.
        Settings.embed_model = OllamaEmbedding(
            model_name=self.valves.LLAMAINDEX_EMBEDDING_MODEL_NAME,
            base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
        )

        Settings.llm = Ollama(
            model=self.valves.LLAMAINDEX_MODEL_NAME,
            base_url=self.valves.LLAMAINDEX_OLLAMA_BASE_URL,
            request_timeout=360.0)
        
        chroma_db = chromadb.HttpClient(host=self.valves.CHROMA_HOST, port=self.valves.CHROMA_PORT)

        todays_info_engine = FunctionTool.from_defaults(
            fn=self.current_date,
            name="todays_info_engine",
            description="This tool provides information about the current date and time"
        )

        code_spec = CodeInterpreterToolSpec()

        tools = []
        tools.append(todays_info_engine)
        tools.append(code_spec.to_tool_list()[0])
        try:
            logging.info(f"Chroma client is connected")
            chroma_collection = chroma_db.get_collection("alfred")
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            index = VectorStoreIndex.from_vector_store(vector_store)
            query_engine = index.as_query_engine(llm=Settings.llm)

            email_reader_engine = QueryEngineTool(
                query_engine=query_engine,
                metadata=ToolMetadata(
                    name="email_reader",
                    description="This tool can retrieve email content from google mail inbox"
                )
            )
            tools.append(email_reader_engine)
        except Exception as e:
            logging.error(f"An error occurred: {e}")


        self.agent = ReActAgent.from_tools(
            tools=tools, llm=Settings.llm, verbose=True, max_iterations=50)
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom RAG pipeline.
        # Typically, you would retrieve relevant information from your knowledge base and synthesize it to generate a response.


        response = self.agent.query(user_message)


        if isinstance(response, Response):
            return str(response)
        elif isinstance(response, StreamingResponse):
            return response.response_gen
        else:
            return str(response)
