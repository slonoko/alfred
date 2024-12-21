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
from llama_index.core import VectorStoreIndex, StorageContext
from pydantic import BaseModel, Field
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo

from email_reader import GmailReader

gmail_reader = GmailReader(
        use_iterative_parser=False)
gmail_reader.query = "after:2024/01/01 samsun"
emails = gmail_reader.load_data()
print(len(emails))
 
""" documents = None
index = None

Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-m3")
Settings.llm = Ollama(model="llama3.2", base_url="http://localhost:11434",request_timeout=360.0)

chroma_client = chromadb.HttpClient(host="localhost", port=8000) 
print("Chroma is connected? " + str(chroma_client.heartbeat()>0))

chroma_collection = chroma_client.get_collection("alfred")


vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store)

vector_store_info = VectorStoreInfo(
    content_info="Content of emails",
    metadata_info=[
        MetadataInfo(
            name="email_reader_engine",
            type="str",
            description=(
                "Primary tool to search through emails for information and answer questions."
            ),
        )
    ],
)

retriever = VectorIndexAutoRetriever(
    index, vector_store_info=vector_store_info, verbose=True, llm=Settings.llm
)
print("searching ...\n")
retriever.retrieve("did i travel to rhodos?") """