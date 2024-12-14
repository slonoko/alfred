"""
title: String Inverse
author: Your Name
author_url: https://website.com
git_url: https://github.com/username/string-reverse.git
description: This tool calculates the inverse of a string
required_open_webui_version: 0.4.0
requirements: llama-index,chromadb,llama-index-vector-stores-chroma,llama-index-core,llama-index-llms-ollama,llama-index-embeddings-huggingface
version: 0.4.0
licence: MIT
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

from pydantic import BaseModel, Field

class Tools:
    def __init__(self):
        """Initialize the Tool."""
        self.documents = None
        self.index = None

    class Valves(BaseModel):
        pass

    async def query_email(self, query: str) -> str:
        """
        search in the email database
        :param query: the text to use to query the email database
        """
        chroma_client = chromadb.HttpClient(host="chromadb", port=8000) 
        logging.info(f"Chroma client is connected")
        chroma_collection = chroma_client.get_collection("alfred")
        return await chroma_collection.query(
            n_results= 10,
            where= {"metadata_field": "is_equal_to_this"},
            query_texts= [query],
            )