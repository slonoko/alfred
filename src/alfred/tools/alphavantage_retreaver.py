import requests
from llama_index.core.tools.tool_spec.base import BaseToolSpec
import logging
from dotenv import load_dotenv
import os
from alfred.utils.semantic_search import perform_search

load_dotenv()


class AlphaVantageToolSpec(BaseToolSpec):
    """
    AlphaVantageToolSpec is a tool specification class for interacting with the Alpha Vantage API. 
    It provides methods to retrieve available functions and execute them using the API. 
    The `get_available_functions` method returns all possible functions related to stocks along with their parameters, which can be used as input for the `execute_function` method to query the Alpha Vantage API.
    Based on the description of the function, select the appropriate parameters and pass them as a dictionary to the `execute_function` method to get the desired data from the API.
    You do not need to pass the apikey as it is automatically included in the request.

    """

    spec_functions = [
        "get_relevant_functions",
        "execute_function",
        "get_apikey"
    ]

    def __init__(self):
        self.api_url = "https://www.alphavantage.co/query"
        self.apikey = os.getenv("ALPHA_VANTAGE_KEY")

        logging.debug("Alpha Vantage tool initialized.")
        logging.debug(f"API URL: {self.api_url}")
        logging.debug(f"API_KEY: {self.apikey}")

    def get_apikey(self):
        """
        Retrieve the API key used to access the Alpha Vantage API.
        """
        logging.debug(f"Retrieving the API_KEY: {self.apikey}")
        return self.apikey

    def get_relevant_functions(self, query):
        """
        Retrieve the relevant function related to query along with the description, parameters and example calls.
        """
        logging.debug(f"Retrieving relevant functions for query: {query}")
        result = perform_search(query)
        logging.debug(f"Relevant functions: {result}")
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
        parameters = parameters or {}
        parameters.update({"apikey": self.apikey}, {"function":function})
        logging.debug(f"Executing function with URL: {base_url}, and Request parameters: {parameters}")
        response = requests.get(base_url, params=parameters)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(
                f"Failed to retrieve data from Alpha Vantage. Status code: {response.status_code}"
            )
            return {}
