from llama_index.embeddings.ollama import OllamaEmbedding
from alfred.utils.semantic_search import available_functions, perform_search

perform_search(available_functions(), "stock price of NVIDIA")