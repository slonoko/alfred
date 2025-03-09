import pytest
from alfred.utils.common import perform_search, initialize_ollama_services, create_index
from alfred.tools.alphavantage_retreaver import AlphaVantageToolSpec
from alfred.utils.alphavantage import AlphaVantageUtils
import logging
from dotenv import load_dotenv
import nest_asyncio

load_dotenv()
nest_asyncio.apply()

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

@pytest.mark.asyncio
async def test_create_index():
    fct = AlphaVantageUtils()
    model, embedding_model, _= initialize_ollama_services("llama3.1")
    await create_index(embedding_model=embedding_model, available_fcts=fct.available_functions(title_only=False))

if __name__ == '__main__':
    pytest.main()