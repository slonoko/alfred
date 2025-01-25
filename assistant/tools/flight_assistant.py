from llama_index.core.tools.tool_spec.base import BaseToolSpec
import requests
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()

class FlightAssistantTool(BaseToolSpec):
    """Flight Assistant tool spec.

    """
    spec_functions = ["search_flights"]

    def __init__(self):
        self.url = "https://sky-scanner3.p.rapidapi.com/flights/price-calendar-web"

        self.headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": os.getenv("RAPIDAPI_HOST")
        }


    def search_flights(self, from_airport_code="FRA", to_airport_code="STR", year_month="2025-03"):
        """
        A usefull function that takes as input the source airport code, destination airport code, and the month of the year (format YYYY-MM) and returns the flights data in json format.
        """
        logging.info(f"Searching flights from {from_airport_code} to {to_airport_code} for the month {year_month}")

        querystring = {"fromEntityId":from_airport_code,"toEntityId":to_airport_code,"yearMonth":year_month,"currency":"EUR"}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        return response.json()