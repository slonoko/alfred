"""
title: Alfred Pipeline
author: Elie Khoury
date: 2024-10-23
version: 1.0
license: MIT
description: A pipeline for retrieving relevant information from a knowledge base using the Llama Index library.
requirements: llama-index,chromadb,llama-index-vector-stores-chroma,llama-index-core,llama-index-llms-ollama,llama-index-embeddings-huggingface,llama-index-embeddings-ollama
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
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.base.response.schema import Response, StreamingResponse
from llama_index.embeddings.ollama import OllamaEmbedding

class Pipeline:
    def __init__(self):
        self.documents = None
        self.index = None

    def current_date(self, **kwargs) -> str:
        return f'Current date is {datetime.datetime.now().strftime("%A, %B %d, %Y")}, and time {datetime.datetime.now().strftime("%H:%M:%S")}'

    async def on_startup(self):
        # This function is called when the server is started.
        ollama_embedding = OllamaEmbedding(
            model_name="nomic-embed-text",
            base_url="http://localhost:11434"
        )

        ollama_llm = Ollama(model="llama3.2", base_url="http://localhost:11434", request_timeout=360.0)
        
        try:
            Settings.embed_model = ollama_embedding
            Settings.llm = ollama_llm
        except Exception as e:
            logging.error(f"An error occurred while setting LLM: {e}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom RAG pipeline.
        # Typically, you would retrieve relevant information from your knowledge base and synthesize it to generate a response.

        todays_info_engine = FunctionTool.from_defaults(
            fn=self.current_date,
            name="todays_info_engine",
            description="This tool provides information about the current date and time"
        )

        tools = []
        tools.append(todays_info_engine)
        try:
            chroma_client = chromadb.HttpClient(host="localhost", port=8000) # .PersistentClient(path="./.storage/alfred_db")
            logging.info(f"Chroma client is connected")
            chroma_collection = chroma_client.get_collection("alfred")
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            index = VectorStoreIndex.from_vector_store(vector_store)
            query_engine = index.as_query_engine(llm=Settings.llm)
            email_reader_engine = QueryEngineTool(
                query_engine=query_engine,
                metadata=ToolMetadata(
                    name="email_reader_engine",
                    description="This tool can retrieve email content from google mail inbox"
                )
            )
            tools.append(email_reader_engine)
        except Exception as e:
            logging.error(f"An error occurred: {e}")


        agent = ReActAgent.from_tools(
            tools=tools, llm=Settings.llm, verbose=True, max_iterations=50)
        response = agent.query(user_message)


        if isinstance(response, Response):
            return str(response)
        elif isinstance(response, StreamingResponse):
            return response.response_gen
        else:
            return str(response)
