import requests
from llama_index.core.tools.tool_spec.base import BaseToolSpec
import logging
from dotenv import load_dotenv
import os

load_dotenv()


class FinancialDataToolSpec(BaseToolSpec):
    """
    Exchange Rate tool spec."""

    spec_functions = [
        "get_news_list",
        "search_news",
        "get_page_content_by_url",
        "get_market_data",
        "get_stock_overview",
        "get_stock_news",
        "get_stock_analysis",
        "get_stock_technical_analysis",
        "get_stock_history_price_chart",
        "get_stock_info",
        "get_stock_dividends",
        "get_stock_splits",
        "get_stock_earnings",
        "get_eps_trend",
        "get_earnings_dates",
        "get_earnings_estimate",
        "get_growth_estimate",
        "get_analyst_price_targets",
        "get_income_statement",
        "get_cash_flow",
        "get_balance_sheet",
        "get_supported_countries",
    ]

    def __init__(self):
        self.api_url = "https://investing11.p.rapidapi.com/"
        self.headers = {
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "x-rapidapi-host": os.getenv("RAPIDAPI_HOST"),
        }

    def get_news_list(self, news_type: str = "latest"):
        """
        news_type parameter can be: latest, popular, crypto, stock_markets, commodities, currencies, economy, economic_indicators, politics, world
        """

        querystring = {"news_type": news_type, "page": "1"}

        response = requests.get(
            f"{self.api_url}get_news", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def search_news(self, query: str):
        """
        Search for news by keyword.
        """

        querystring = {"query": query}

        response = requests.get(
            f"{self.api_url}search_news", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_page_content_by_url(self, url: str):
        """
        Get the content of the page by URL.
        """

        querystring = {"url": url}

        response = requests.get(
            f"{self.api_url}get_page_content_by_url",
            headers=self.headers,
            params=querystring,
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_market_data(self, data_type: str, country: str = "US"):
        """
        Get market data by type and country.
        data_type can have either of the following values: indices, stocks, commodities, currencies, crypto, etfs, funds
        """

        querystring = {"data_type": data_type, "country": country}

        response = requests.get(
            f"{self.api_url}get_market_data", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_stock_overview(self, symbol: str):
        """
        Get the stock overview by symbol, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}get_stock_overview",
            headers=self.headers,
            params=querystring,
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_stock_news(self, symbol: str):
        """
        Get the stock news by symbol, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}get_stock_news", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_stock_analysis(self, symbol: str):
        """
        Get the stock analysis by symbol, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol, "page": 1}

        response = requests.get(
            f"{self.api_url}get_stock_analysis",
            headers=self.headers,
            params=querystring,
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_stock_technical_analysis(self, symbol: str):
        """
        Get the stock technical analysis by symbol, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}get_stock_technical_analysis",
            headers=self.headers,
            params=querystring,
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_stock_history_price_chart(
        self, symbol: str, period: str = "1d", interval: str = "1m"
    ):
        """
        Get the stock history price chart by symbol, example NVDA or Nvidia.
        period can be: 1d, 5d, 1m, 3m, 6m, 1y, 2y, 5y, 10y, ytd, max.
        interval can be: 1m, 5m, 15m, 30m, 1h, 1d, 5d, 1w, 1mo, 3mo.
        """

        querystring = {"symbol": symbol, "period": period, "interval": interval}

        response = requests.get(
            f"{self.api_url}history", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_stock_info(self, symbol: str):
        """
        Get the stock information by symbol, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}info", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_stock_dividends(self, symbol: str):
        """
        Get the stock dividends by symbol, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}dividends", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_stock_splits(self, symbol: str):
        """
        Get the stock splits by symbol, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}splits", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_stock_earnings(self, symbol: str):
        """
        Get the stock earnings by symbol, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}get_stock_earnings",
            headers=self.headers,
            params=querystring,
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_eps_trend(self, symbol: str):
        """
        Get the stock  earning per share trend, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}eps_trend", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_earnings_dates(self, symbol: str):
        """
        Get the stock earning dates, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}earnings_dates", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_earnings_estimate(self, symbol: str):
        """
        Get the stock  earning estimate, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}earnings_estimate", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_growth_estimate(self, symbol: str):
        """
        Get the stock  growth estimate, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}growth_estimate", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_analyst_price_targets(self, symbol: str):
        """
        Get the stock analyst price targets, example NVDA or Nvidia.
        """

        querystring = {"symbol": symbol}

        response = requests.get(
            f"{self.api_url}analyst_price_targets",
            headers=self.headers,
            params=querystring,
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_income_statement(self, symbol: str, type: str = "annual"):
        """
        Get the stock income statement, example NVDA or Nvidia.
        type can be: annual, quarterly
        """

        querystring = {"symbol": symbol, "type": type}

        response = requests.get(
            f"{self.api_url}income_statement", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_cash_flow(self, symbol: str, type: str = "annual"):
        """
        Get the stock cash flow, example NVDA or Nvidia.
        type can be: annual, quarterly
        """

        querystring = {"symbol": symbol, "type": type}

        response = requests.get(
            f"{self.api_url}cash_flow", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_balance_sheet(self, symbol: str, type: str = "annual"):
        """
        Get the stock balance sheet, example NVDA or Nvidia.
        type can be: annual, quarterly
        """

        querystring = {"symbol": symbol, "type": type}

        response = requests.get(
            f"{self.api_url}balance_sheet", headers=self.headers, params=querystring
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}

    def get_supported_countries(self):
        """
        Get the list of supported countries.
        """

        querystring = {}

        response = requests.get(
            f"{self.api_url}get_supported_countries",
            headers=self.headers,
            params=querystring,
        )
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {}
