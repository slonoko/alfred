import os 
import logging
import json 
import pickle
from llama_index.embeddings.ollama import OllamaEmbedding
import chromadb

def available_functions(): 
    """ Retrieve the list of functions related to stocks along with the description. """ 
    try: 
        with open("/home/elie/Projects/alfred/src/alfred/tools/functions.json", "r") as file: 
            logging.debug("functions.json loaded.") 
            functions = json.load(file) 
            return [[fct["function"], fct["description"], fct["parameters"]] for fct in functions] 
    except FileNotFoundError: 
        logging.error("functions.json file not found.") 
        return [] 
    except Exception as e: 
        logging.error(f"An error occurred while reading functions.json: {e}") 
        return []

def perform_search(query): 
    client = chromadb.HttpClient("khoury")
    try:
        collection = client.get_collection("docs")
    except chromadb.errors.InvalidCollectionException as e:
        logging.error(f"Collection not found: {e}")
        collection = client.create_collection("docs", get_or_create=True)

    ollama_embedding = OllamaEmbedding(
        model_name="bge-m3",
        base_url="http://khoury:11434",
        ollama_additional_kwargs={"mirostat": 0},
    )

    for i, d,p in available_functions():
        embeddings = ollama_embedding.get_text_embedding(d)
        collection.add(
            ids=i,
            embeddings=embeddings,
            documents=d,
            metadatas={"parameters":json.dumps(p)},
        )

    # generate an embedding for the input and retrieve the most relevant doc
    query_embeddings = ollama_embedding.get_query_embedding(query)
    results = collection.query(
    query_embeddings=[query_embeddings],
    n_results=3
    )

    matched_id = results["ids"][0][0]
    documentation = results["documents"][0][0]
    parameters = json.loads(results["metadatas"][0][0]["parameters"])
    
    return {"function": matched_id, "documentation": documentation, "parameters": parameters}