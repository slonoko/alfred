import requests
from llama_index.core.tools.tool_spec.base import BaseToolSpec
import logging
from dotenv import load_dotenv
import os

load_dotenv()


class AlphaVantageToolSpec(BaseToolSpec):
    """
    Stocks financial data tool spec."""

    spec_functions = [
        "get_available_functions",
        "get_apikey",
        "execute_function",
    ]

    def __init__(self):
        self.api_url = "https://www.alphavantage.co/query"
        self.apikey = os.getenv("ALPHA_VANTAGE_KEY")

        logging.debug("Financial data tool initialized.")
        logging.debug(f"API URL: {self.api_url}")
        logging.debug(f"API_KEY: {self.apikey}")

    def get_apikey(self):
        return self.apikey
    
    def get_available_functions(self):
        """
        Retrieve the list of operations related to stocks along with the input and example calls.
        """
        try:
            with open("functions.json", "r") as file:
                return file.read()
        except FileNotFoundError:
            logging.error("functions.json file not found.")
            return {}
        except Exception as e:
            logging.error(f"An error occurred while reading functions.json: {e}")
            return {}

    def execute_function(
        self, parameters: dict = None
    ):
        """
        Retrieve information from Alpha Vantage server.
        :param parameters: A dictionary of parameters. The list of parameters can be found in the Alpha Vantage json extracted from the read_functions_json method.
        :return: The response data from Alpha Vantage.
        """
        base_url = self.api_url
        logging.debug(f"Generated URL: {base_url}")
        logging.debug(f"Request parameters: {parameters}")
        response = requests.get(base_url, params=parameters)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(
                f"Failed to retrieve data from Alpha Vantage. Status code: {response.status_code}"
            )
            return {}
