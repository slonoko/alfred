"""Email contect retriever tool spec"""

import datetime
from llama_index.tools.vector_db.base import VectorDBToolSpec
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core import VectorStoreIndex

class EmailRetrieverSpec(VectorDBToolSpec):
    pass