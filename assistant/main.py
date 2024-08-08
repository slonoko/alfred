from llama_index.core import VectorStoreIndex, Settings, StorageContext, load_index_from_storage
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.milvus import MilvusVectorStore
from gmail import GmailReader

import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3") # https://huggingface.co/BAAI/bge-m3
# Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

gmail_reader = GmailReader(results_per_page=100, max_results=100, use_iterative_parser=True)

# check if storage already exists
PERSIST_DIR = "./.storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    emails = gmail_reader.load_data()
    os.mkdir(".storage")
    vector_store = MilvusVectorStore(
    uri="./.storage/mails.db", dim=1024, overwrite=True
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        emails, storage_context=storage_context
    )
else: 
    # load the existing index
    vector_store = MilvusVectorStore(uri="./.storage/mails.db", dim=1024)
    index = VectorStoreIndex.from_vector_store(vector_store)

chat_engine = index.as_chat_engine(chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT)
chat_engine.reset()
command = input("Q: ")
while(command != "exit"):
    print(
        chat_engine.chat(
            command
        )
    )
    command = input("Q: ")