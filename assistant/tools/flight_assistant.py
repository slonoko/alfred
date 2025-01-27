from llama_index.core.tools.tool_spec.base import BaseToolSpec
import requests
import logging
from dotenv import load_dotenv
import os

load_dotenv()


class FlightAssistantTool(BaseToolSpec):
    """Flight Assistant tool spec."""

    spec_functions = [
        "oneway_flights_month",
        "twoway_flights_month",
        "airports_information",
        "one_way_flight",
        "round_trip_flight",
    ]

    def __init__(self):
        self.url = "https://sky-scanner3.p.rapidapi.com/flights/"

        self.headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": os.getenv("RAPIDAPI_HOST"),
        }

    def oneway_flights_month(
        self, from_airport_code="FRA", to_airport_code="STR", year_month="2025-03"
    ):
        """
        A usefull function that takes as input the source airport code, destination airport code, and the month of the year (format YYYY-MM) and returns the flights data in json format.
        """
        logging.debug(
            f"Searching flights from {from_airport_code} to {to_airport_code} for the month {year_month}"
        )

        querystring = {
            "fromEntityId": from_airport_code,
            "toEntityId": to_airport_code,
            "yearMonth": year_month,
            "currency": "EUR",
        }
        response = requests.get(
            f"{self.url}price-calendar-web", headers=self.headers, params=querystring
        )
        return response.json()

    def twoway_flights_month(
        self,
        from_airport_code="FRA",
        to_airport_code="STR",
        year_month="2025-03",
        return_year_month="2025-04",
    ):
        """
        A usefull function that takes as input the source airport code, destination airport code, and the month of the year (format YYYY-MM) and returns the flights data in json format.
        """
        logging.debug(
            f"Searching flights from {from_airport_code} to {to_airport_code} for the month {year_month}, and returning on {return_year_month}"
        )

        querystring = {
            "fromEntityId": from_airport_code,
            "toEntityId": to_airport_code,
            "yearMonth": year_month,
            "yearMonthReturn": return_year_month,
            "currency": "EUR",
        }
        response = requests.get(
            f"{self.url}price-calendar-web-return",
            headers=self.headers,
            params=querystring,
        )
        return response.json()

    def airports_information(self):
        """
        A usefull function that returns the list of airports and their information in json format.
        """
        logging.debug(f"Searching for airports information")

        querystring = {}
        response = requests.get(
            f"{self.url}airports", headers=self.headers, params=querystring
        )
        return response.json()

    def one_way_flight(
        self,
        from_airport_code="FRA",
        to_airport_code="STR",
        depart_date="2025-03",
        stops="direct",
        children="0",
        infants="0",
        cabinClass="economy",
        adults="2",
        includeOriginNearbyAirports="false",
        includeDestinationNearbyAirports="false",
        airlines=None
    ):
        """
        A usefull function that searches for one way flights based on multiple parameters and returns the flights data in json format.
        Important to note that the parameter:
        - cabinClass can take exclusively one of the following values: economy, premium_economy, business, first
        - stops can take one or more of the following values: direct, 1stop, 2stops
        - airlines can be retrieved from response this endpoint(data->filterStats->carriers->id), and It can input multiple values, and the values should be separated by commas. Ex: -32753,-32695,-32677
        - includeOriginNearbyAirports and includeDestinationNearbyAirports can take the values: true, false
        """

        logging.debug(
            f"Searching for one way flights from {from_airport_code} to {to_airport_code} for the depart date {depart_date}"
        )

        querystring = {
            "fromEntityId": from_airport_code,
            "toEntityId": to_airport_code,
            "departDate": depart_date,
            "currency": "EUR",
            "stops": stops,
            "children": children,
            "infants": infants,
            "cabinClass": cabinClass,
            "adults": adults,
            "includeOriginNearbyAirports": includeOriginNearbyAirports,
            "includeDestinationNearbyAirports": includeDestinationNearbyAirports,
            "sort": "cheapest_first",
            "airlines": airlines,
        }
        response = requests.get(
            f"{self.url}search-one-way",
            headers=self.headers,
            params=querystring,
        )
        return response.json()

    def round_trip_flight(
        self,
        from_airport_code="FRA",
        to_airport_code="STR",
        depart_date="2025-03",
        return_date="2025-04",
        stops="direct",
        children="0",
        infants="0",
        cabinClass="economy",
        adults="2",
        includeOriginNearbyAirports="false",
        includeDestinationNearbyAirports="false",
        airlines=None
    ):
        """
        A usefull function that searches for round trip flights based on multiple parameters and returns the flights data in json format.
        Important to note that the parameter:
        - cabinClass can take exclusively one of the following values: economy, premium_economy, business, first
        - stops can take one or more of the following values: direct, 1stop, 2stops
        - airlines can be retrieved from response this endpoint(data->filterStats->carriers->id), and It can input multiple values, and the values should be separated by commas. Ex: -32753,-32695,-32677
        - includeOriginNearbyAirports and includeDestinationNearbyAirports can take the values: true, false
        """

        logging.debug(
            f"Searching for round trip flights from {from_airport_code} to {to_airport_code} for the depart date {depart_date} and returning on {return_date}"
        )

        querystring = {
            "fromEntityId": from_airport_code,
            "toEntityId": to_airport_code,
            "departDate": depart_date,
            "returnDate": return_date,
            "currency": "EUR",
            "stops": stops,
            "children": children,
            "infants": infants,
            "cabinClass": cabinClass,
            "adults": adults,
            "includeOriginNearbyAirports": includeOriginNearbyAirports,
            "includeDestinationNearbyAirports": includeDestinationNearbyAirports,
            "sort": "cheapest_first",
            "airlines": airlines,
        }
        response = requests.get(
            f"{self.url}search-roundtrip",
            headers=self.headers,
            params=querystring,
        )
        return response.json()
