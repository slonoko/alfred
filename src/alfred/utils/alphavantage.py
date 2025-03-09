import requests
from llama_index.core.tools.tool_spec.base import BaseToolSpec
import logging
from dotenv import load_dotenv
import os
from alfred.utils.common import perform_search, create_index, search_index
import json
from llama_index.core import Settings

load_dotenv()


class AlphaVantageUtils():

    def __init__(self):
        self.api_url = os.getenv("ALPHA_VANTAGE_URL")
        self.apikey = os.getenv("ALPHA_VANTAGE_KEY")

        logging.info("Alpha Vantage tool initialized.")

    def get_apikey(self):
        """
        Retrieve the API key used to access the Alpha Vantage API.
        """
        logging.info(f"Retrieving the API_KEY: {self.apikey}")
        return self.apikey
    
    def available_functions(self, title_only=False): 
        """ Retrieve the list of functions related to stocks along with the description. """ 
        try: 
            with open(os.getenv("fcts_path"), "r") as file: 
                logging.info("functions.json loaded.") 
                functions = json.load(file) 
                if title_only:
                    return [[fct["function"], fct["description"]] for fct in functions]
                else:
                    return [[fct["function"], fct["description"], fct["parameters"]] for fct in functions]
        except FileNotFoundError: 
            logging.error("functions.json file not found.") 
            return [] 
        except Exception as e: 
            logging.error(f"An error occurred while reading functions.json: {e}") 
            return []

    async def get_relevant_functions(self, query):
        """
        Retrieve the relevant function related to query along with the description, parameters and example calls.
        """
        logging.info(f"Retrieving relevant functions for query: {query}")
        result = await search_index(query=query)
        logging.info(f"Relevant functions: {result['function']}")
        return result

    def execute_function(
        self, function: str, parameters: dict = None
    ):
        """
        Retrieve information from Alpha Vantage server. No need to pass the apikey as it is automatically included in the request.
        :param function: The function name to be executed. The function can be selected from the list of functions in the json extracted from the get_available_functions method, based on the description of the function.
        :param parameters: A JSON object of parameters of key-value pair format, where the key if the parameter name. The list of parameters can be found in the Alpha Vantage json extracted from the read_functions_json method.
        :return: The response data from Alpha Vantage.
        """
        base_url = self.api_url
        
        # Add the apikey and function to the parameters
        _parameters = parameters or {}
        _parameters.update({"function":function})
        _parameters.update({"apikey":self.apikey})
        logging.info(f"Executing function with URL: {base_url}, and Request parameters: {_parameters}")
        response = requests.get(base_url, params=_parameters)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(
                f"Failed to retrieve data from Alpha Vantage. Status code: {response.status_code}"
            )
            return {}
