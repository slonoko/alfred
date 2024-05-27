from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.core.chat_engine.types import ChatMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from gmail import GmailReader

import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# bge-base embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5") # BAAI/bge-m3

# ollama
Settings.llm = Ollama(model="llama3", request_timeout=360.0)

gmail_reader = GmailReader(results_per_page=50, max_results=1000, use_iterative_parser=True)

# check if storage already exists
PERSIST_DIR = "./.storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    #documents = SimpleDirectoryReader(".data").load_data()
    emails = gmail_reader.load_data()

    index = VectorStoreIndex.from_documents(emails) #.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else: 
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)



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