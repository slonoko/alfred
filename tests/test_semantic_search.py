import pytest
from alfred.utils.common import perform_search, initialize_ollama_services
from alfred.tools.alphavantage_retreaver import AlphaVantageToolSpec
import logging
from dotenv import load_dotenv

load_dotenv()

def setup_module(module):
    ''' Setup for the entire module '''
    pass

def setup_function(func):
    ''' Setup for test functions '''
    pass

def test_perform_search_not_none():
    query = "NVDA current stock price?"
    fct = AlphaVantageToolSpec()
    model, embedding_model, _= initialize_ollama_services("llama3.1")
    result = perform_search(embedding_model,fct.available_functions(), query)
    logging.info(f"Result: {result}")
    assert result is not None  # Check that the result is not None

if __name__ == '__main__':
    pytest.main()