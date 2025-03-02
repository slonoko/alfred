import requests
from llama_index.core.tools.tool_spec.base import BaseToolSpec

class ExchangeRateTool(BaseToolSpec):
    """
    Exchange Rate tool spec."""

    spec_functions = ["get_exchange_rates", "convert"]

    def __init__(self):
        self.api_url = "https://api.exchangerate-api.com/v4/latest/"

    def get_exchange_rates(self, from_currency='USD'):
        """
        Get exchange rates for a given currency."""

        response = requests.get(f'{self.api_url}{from_currency}')
        if response.status_code == 200:
            return response.json().get('rates', {})
        else:
            return {}

    def convert(self, amount, from_currency="USD", to_currency="EUR"):
        """
        Convert an amount from one currency to another."""

        rates = self.get_exchange_rates(from_currency)
        if to_currency in rates:
            return amount * rates[to_currency]
        else:
            raise ValueError(f"Currency {to_currency} not supported.")