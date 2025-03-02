import os 
from sentence_transformers import SentenceTransformer, util
import logging
import json 
import pickle


def available_functions(): 
    """ Retrieve the list of functions related to stocks along with the description. """ 
    try: 
        with open("./assistant/tools/functions.json", "r") as file: 
            logging.debug("functions.json loaded.") 
            functions = json.load(file) 
            return [(fct["function"], fct["description"]) for fct in functions] 
    except FileNotFoundError: 
        logging.error("functions.json file not found.") 
        return [] 
    except Exception as e: 
        logging.error(f"An error occurred while reading functions.json: {e}") 
        return []

def perform_search(corpus, query): 
    embedder = SentenceTransformer("BAAI/bge-m3") # sentence-transformers/all-mpnet-base-v2
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    # Query sentences: 
    queries = [query]
    for query in queries: 
        if not os.path.exists("./av_functions.pkl"): 
            query_embedding = embedder.encode(query, convert_to_tensor=True) 
            with open("av_functions.pkl", "wb") as fOut: 
                pickle.dump(query_embedding,fOut) 
        else: 
                with open("av_functions.pkl", "rb") as fIn: 
                    query_embedding = pickle.load(fIn)
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=10) 
    hits = hits[0] 
    # Get the hits for the first query 
    for hit in hits: 
        print(corpus[hit["corpus_id"]], "(Score: {:.4f})".format(hit["score"]))