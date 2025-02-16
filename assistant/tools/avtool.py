import requests
from llama_index.core.tools.tool_spec.base import BaseToolSpec
import logging
from dotenv import load_dotenv
import os

load_dotenv()


class AVToolSpec(BaseToolSpec):
    """
    AVToolSpec is a tool specification class for interacting with the Alpha Vantage API.    
    """

    spec_functions = [
        'time_series_intraday',
        'time_series_daily',
        'time_series_daily_adjusted',
        'time_series_weekly',
        'time_series_weekly_adjusted',
        'time_series_monthly',
        'time_series_monthly_adjusted',
        'global_quote',
        'realtime_bulk_quotes',
        'symbol_search',
        'market_status',
        'realtime_options',
        'historical_options',
        'news_sentiment',
        'top_gainers_losers',
        'insider_transactions',
        'analytics_fixed_window',
        'analytics_sliding_window',
        'overview',
        'etf_profile',
        'dividends',
        'splits',
        'income_statement',
        'balance_sheet',
        'cash_flow',
        'earnings',
        'listing_status',
        'earnings_calendar',
        'currency_exchange_rate',
        'crypto_intraday',
        'digital_currency_daily',
        'digital_currency_weekly',
        'digital_currency_monthly',
        'fx_intraday',
        'fx_daily',
        'fx_weekly',
        'brent',
        'natural_gas',
        'copper',
        'aluminum',
        'wheat',
        'corn',
        'cotton',
        'sugar',
        'coffee',
        'all_commodities',
        'real_gdp',
        'real_gdp_per_capita',
        'treasury_yield',
        'federal_funds_rate',
        'cpi',
        'inflation',
        'retail_sales',
        'durables',
        'unemployment',
        'nonfarm_payroll',
        'sma',
        'ema',
        'wma'
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

    def call_api(self, params):
        """
        Helper function to call the Alpha Vantage API with the given parameters.
        """
        params['apikey'] = self.get_apikey()
        response = requests.get(self.api_url, params=params)
        return response.json()

    def time_series_intraday(self, symbol, interval, adjusted=True, extended_hours=True, month=None, outputsize='compact', datatype='json'):
        """
        TIME_SERIES_INTRADAY function.
        This API returns current and 20+ years of historical intraday OHLCV time series of the equity specified, covering pre-market and post-market hours where applicable.
        """
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'adjusted': adjusted,
            'extended_hours': extended_hours,
            'month': month,
            'outputsize': outputsize,
            'datatype': datatype
        }
        return self.call_api(params)

    def time_series_daily(self, symbol, outputsize='compact', datatype='json'):
        """
        TIME_SERIES_DAILY function.
        This API returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, covering 20+ years of historical data.
        """
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': outputsize,
            'datatype': datatype
        }
        return self.call_api(params)

    def time_series_daily_adjusted(self, symbol, outputsize='compact', datatype='json'):
        """
        TIME_SERIES_DAILY_ADJUSTED function.
        This API returns raw (as-traded) daily open/high/low/close/volume values, adjusted close values, and historical split/dividend events of the global equity specified, covering 20+ years of historical data.
        """
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': symbol,
            'outputsize': outputsize,
            'datatype': datatype
        }
        return self.call_api(params)

    def time_series_weekly(self, symbol, datatype='json'):
        """
        TIME_SERIES_WEEKLY function.
        This API returns weekly time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly volume) of the global equity specified, covering 20+ years of historical data.
        """
        params = {
            'function': 'TIME_SERIES_WEEKLY',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def time_series_weekly_adjusted(self, symbol, datatype='json'):
        """
        TIME_SERIES_WEEKLY_ADJUSTED function.
        This API returns weekly adjusted time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly adjusted close, weekly volume, weekly dividend) of the global equity specified, covering 20+ years of historical data.
        """
        params = {
            'function': 'TIME_SERIES_WEEKLY_ADJUSTED',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def time_series_monthly(self, symbol, datatype='json'):
        """
        TIME_SERIES_MONTHLY function.
        This API returns monthly time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly volume) of the global equity specified, covering 20+ years of historical data.
        """
        params = {
            'function': 'TIME_SERIES_MONTHLY',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def time_series_monthly_adjusted(self, symbol, datatype='json'):
        """
        TIME_SERIES_MONTHLY_ADJUSTED function.
        This API returns monthly adjusted time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly adjusted close, monthly volume, monthly dividend) of the equity specified, covering 20+ years of historical data.
        """
        params = {
            'function': 'TIME_SERIES_MONTHLY_ADJUSTED',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def global_quote(self, symbol, datatype='json'):
        """
        GLOBAL_QUOTE function.
        This endpoint returns the latest price and volume information for a ticker of your choice. You can specify one ticker per API request.
        """
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def realtime_bulk_quotes(self, symbol, datatype='json'):
        """
        REALTIME_BULK_QUOTES function.
        This API returns realtime quotes for US-traded symbols in bulk, accepting up to 100 symbols per API request and covering both regular and extended (pre-market and post-market) trading hours.
        """
        params = {
            'function': 'REALTIME_BULK_QUOTES',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def symbol_search(self, keywords, datatype='json'):
        """
        SYMBOL_SEARCH function.
        This API returns the best-matching symbols and market information based on keywords of your choice.
        """
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords,
            'datatype': datatype
        }
        return self.call_api(params)

    def market_status(self, datatype='json'):
        """
        MARKET_STATUS function.
        This API returns the current market status (open, closed, or upcoming) for a global stock exchange of your choice.
        """
        params = {
            'function': 'MARKET_STATUS',
            'datatype': datatype
        }
        return self.call_api(params)

    def realtime_options(self, symbol, contract=None, datatype='json'):
        """
        REALTIME_OPTIONS function.
        This API returns realtime US options data with full market coverage. Option chains are sorted by expiration dates in chronological order. Within the same expiration date, contracts are sorted by strike prices from low to high.
        """
        params = {
            'function': 'REALTIME_OPTIONS',
            'symbol': symbol,
            'contract': contract,
            'datatype': datatype
        }
        return self.call_api(params)

    def historical_options(self, symbol, date=None, datatype='json'):
        """
        HISTORICAL_OPTIONS function.
        This API returns the full historical options chain for a specific symbol on a specific date, covering 15+ years of history. Implied volatility (IV) and common Greeks (e.g., delta, gamma, theta, vega, rho) are also returned. Option chains are sorted by expiration dates in chronological order. Within the same expiration date, contracts are sorted by strike prices from low to high.
        """
        params = {
            'function': 'HISTORICAL_OPTIONS',
            'symbol': symbol,
            'date': date,
            'datatype': datatype
        }
        return self.call_api(params)

    def news_sentiment(self, tickers=None, topics=None, time_from=None, time_to=None, sort='LATEST', limit=50, datatype='json'):
        """
        NEWS_SENTIMENT function.
        This API returns live and historical market news & sentiment data from a large & growing selection of premier news outlets around the world, covering stocks, cryptocurrencies, forex, and a wide range of topics such as fiscal policy, mergers & acquisitions, IPOs, etc.
        """
        params = {
            'function': 'NEWS_SENTIMENT',
            'tickers': tickers,
            'topics': topics,
            'time_from': time_from,
            'time_to': time_to,
            'sort': sort,
            'limit': limit,
            'datatype': datatype
        }
        return self.call_api(params)

    def top_gainers_losers(self, datatype='json'):
        """
        TOP_GAINERS_LOSERS function.
        This endpoint returns the top 20 gainers, losers, and the most active traded tickers in the US market.
        """
        params = {
            'function': 'TOP_GAINERS_LOSERS',
            'datatype': datatype
        }
        return self.call_api(params)

    def insider_transactions(self, symbol, datatype='json'):
        """
        INSIDER_TRANSACTIONS function.
        This API returns the latest and historical insider transactions made by key stakeholders (e.g., founders, executives, board members, etc.) of a specific company.
        """
        params = {
            'function': 'INSIDER_TRANSACTIONS',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def analytics_fixed_window(self, symbols, range, oHLC='close', interval='DAILY', calculations='MEAN', datatype='json'):
        """
        ANALYTICS_FIXED_WINDOW function.
        This endpoint returns a rich set of advanced analytics metrics (e.g., total return, variance, autocorrelation, etc.) for a given time series over a fixed temporal window.
        """
        params = {
            'function': 'ANALYTICS_FIXED_WINDOW',
            'symbols': symbols,
            'range': range,
            'oHLC': oHLC,
            'interval': interval,
            'calculations': calculations,
            'datatype': datatype
        }
        return self.call_api(params)

    def analytics_sliding_window(self, symbols, range, oHLC='close', interval='DAILY', window_size=20, calculations='MEAN', datatype='json'):
        """
        ANALYTICS_SLIDING_WINDOW function.
        This endpoint returns a rich set of advanced analytics metrics (e.g., total return, variance, autocorrelation, etc.) for a given time series over sliding time windows.
        """
        params = {
            'function': 'ANALYTICS_SLIDING_WINDOW',
            'symbols': symbols,
            'range': range,
            'oHLC': oHLC,
            'interval': interval,
            'window_size': window_size,
            'calculations': calculations,
            'datatype': datatype
        }
        return self.call_api(params)

    def overview(self, symbol, datatype='json'):
        """
        OVERVIEW function.
        This API returns the company information, financial ratios, and other key metrics for the equity specified. Data is generally refreshed on the same day a company reports its latest earnings and financials.
        """
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def etf_profile(self, symbol, datatype='json'):
        """
        ETF_PROFILE function.
        This API returns key ETF metrics (e.g., net assets, expense ratio, and turnover), along with the corresponding ETF holdings / constituents with allocation by asset types and sectors.
        """
        params = {
            'function': 'ETF_PROFILE',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def dividends(self, symbol, datatype='json'):
        """
        DIVIDENDS function.
        This API returns historical and future (declared) dividend distributions.
        """
        params = {
            'function': 'DIVIDENDS',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def splits(self, symbol, datatype='json'):
        """
        SPLITS function.
        This API returns historical split events.
        """
        params = {
            'function': 'SPLITS',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def income_statement(self, symbol, datatype='json'):
        """
        INCOME_STATEMENT function.
        This API returns the annual and quarterly income statements for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports its latest earnings and financials.
        """
        params = {
            'function': 'INCOME_STATEMENT',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def balance_sheet(self, symbol, datatype='json'):
        """
        BALANCE_SHEET function.
        This API returns the annual and quarterly balance sheets for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports its latest earnings and financials.
        """
        params = {
            'function': 'BALANCE_SHEET',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def cash_flow(self, symbol, datatype='json'):
        """
        CASH_FLOW function.
        This API returns the annual and quarterly cash flow for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports its latest earnings and financials.
        """
        params = {
            'function': 'CASH_FLOW',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def earnings(self, symbol, datatype='json'):
        """
        EARNINGS function.
        This API returns the annual and quarterly earnings (EPS) for the company of interest. Quarterly data also includes analyst estimates and surprise metrics.
        """
        params = {
            'function': 'EARNINGS',
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def listing_status(self, date=None, state='active', datatype='json'):
        """
        LISTING_STATUS function.
        This API returns a list of active or delisted US stocks and ETFs, either as of the latest trading day or at a specific time in history.
        """
        params = {
            'function': 'LISTING_STATUS',
            'date': date,
            'state': state,
            'datatype': datatype
        }
        return self.call_api(params)

    def earnings_calendar(self, horizon=None, symbol=None, datatype='json'):
        """
        EARNINGS_CALENDAR function.
        This API returns the earnings calendar for a company or the broader market.
        """
        params = {
            'function': 'EARNINGS_CALENDAR',
            'horizon': horizon,
            'symbol': symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def currency_exchange_rate(self, from_currency, to_currency, datatype='json'):
        """
        CURRENCY_EXCHANGE_RATE function.
        This API returns the realtime exchange rate for any pair of digital currency (e.g., Bitcoin) or physical currency (e.g., USD).
        """
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': from_currency,
            'to_currency': to_currency,
            'datatype': datatype
        }
        return self.call_api(params)

    def crypto_intraday(self, symbol, market, interval, outputsize='compact', datatype='json'):
        """
        CRYPTO_INTRADAY function.
        This API returns intraday time series (timestamp, open, high, low, close, volume) of the cryptocurrency specified, updated realtime.
        """
        params = {
            'function': 'CRYPTO_INTRADAY',
            'symbol': symbol,
            'market': market,
            'interval': interval,
            'outputsize': outputsize,
            'datatype': datatype
        }
        return self.call_api(params)

    def digital_currency_daily(self, symbol, market, datatype='json'):
        """
        DIGITAL_CURRENCY_DAILY function.
        This API returns the daily historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.
        """
        params = {
            'function': 'DIGITAL_CURRENCY_DAILY',
            'symbol': symbol,
            'market': market,
            'datatype': datatype
        }
        return self.call_api(params)

    def digital_currency_weekly(self, symbol, market, datatype='json'):
        """
        DIGITAL_CURRENCY_WEEKLY function.
        This API returns the weekly historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.
        """
        params = {
            'function': 'DIGITAL_CURRENCY_WEEKLY',
            'symbol': symbol,
            'market': market,
            'datatype': datatype
        }
        return self.call_api(params)

    def digital_currency_monthly(self, symbol, market, datatype='json'):
        """
        DIGITAL_CURRENCY_MONTHLY function.
        This API returns the monthly historical time series for a digital currency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.
        """
        params = {
            'function': 'DIGITAL_CURRENCY_MONTHLY',
            'symbol': symbol,
            'market': market,
            'datatype': datatype
        }
        return self.call_api(params)

    def fx_intraday(self, from_symbol, to_symbol, interval, outputsize='compact', datatype='json'):
        """
        FX_INTRADAY function.
        This API returns intraday time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        """
        params = {
            'function': 'FX_INTRADAY',
            'from_symbol': from_symbol,
            'to_symbol': to_symbol,
            'interval': interval,
            'outputsize': outputsize,
            'datatype': datatype
        }
        return self.call_api(params)

    def fx_daily(self, from_symbol, to_symbol, outputsize='compact', datatype='json'):
        """
        FX_DAILY function.
        This API returns the daily time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        """
        params = {
            'function': 'FX_DAILY',
            'from_symbol': from_symbol,
            'to_symbol': to_symbol,
            'outputsize': outputsize,
            'datatype': datatype
        }
        return self.call_api(params)

    def fx_weekly(self, from_symbol, to_symbol, datatype='json'):
        """
        FX_WEEKLY function.
        This API returns the weekly time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.
        """
        params = {
            'function': 'FX_WEEKLY',
            'from_symbol': from_symbol,
            'to_symbol': to_symbol,
            'datatype': datatype
        }
        return self.call_api(params)

    def brent(self, interval='monthly', datatype='json'):
        """
        BRENT function.
        This API returns the Brent (Europe) crude oil prices in daily, weekly, and monthly horizons.
        """
        params = {
            'function': 'BRENT',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def natural_gas(self, interval='monthly', datatype='json'):
        """
        NATURAL_GAS function.
        This API returns the Henry Hub natural gas spot prices in daily, weekly, and monthly horizons.
        """
        params = {
            'function': 'NATURAL_GAS',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def copper(self, interval='monthly', datatype='json'):
        """
        COPPER function.
        This API returns the global price of copper in monthly, quarterly, and annual horizons.
        """
        params = {
            'function': 'COPPER',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def aluminum(self, interval='monthly', datatype='json'):
        """
        ALUMINUM function.
        This API returns the global price of aluminum in monthly, quarterly, and annual horizons.
        """
        params = {
            'function': 'ALUMINUM',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def wheat(self, interval='monthly', datatype='json'):
        """
        WHEAT function.
        This API returns the global price of wheat in monthly, quarterly, and annual horizons.
        """
        params = {
            'function': 'WHEAT',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def corn(self, interval='monthly', datatype='json'):
        """
        CORN function.
        This API returns the global price of corn in monthly, quarterly, and annual horizons.
        """
        params = {
            'function': 'CORN',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def cotton(self, interval='monthly', datatype='json'):
        """
        COTTON function.
        This API returns the global price of cotton in monthly, quarterly, and annual horizons.
        """
        params = {
            'function': 'COTTON',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def sugar(self, interval='monthly', datatype='json'):
        """
        SUGAR function.
        This API returns the global price of sugar in monthly, quarterly, and annual horizons.
        """
        params = {
            'function': 'SUGAR',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def coffee(self, interval='monthly', datatype='json'):
        """
        COFFEE function.
        This API returns the global price of coffee in monthly, quarterly, and annual horizons.
        """
        params = {
            'function': 'COFFEE',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def all_commodities(self, interval='monthly', datatype='json'):
        """
        ALL_COMMODITIES function.
        This API returns the global price index of all commodities in monthly, quarterly, and annual temporal dimensions.
        """
        params = {
            'function': 'ALL_COMMODITIES',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def real_gdp(self, interval='annual', datatype='json'):
        """
        REAL_GDP function.
        This API returns the annual and quarterly Real GDP of the United States.
        """
        params = {
            'function': 'REAL_GDP',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def real_gdp_per_capita(self, datatype='json'):
        """
        REAL_GDP_PER_CAPITA function.
        This API returns the quarterly Real GDP per Capita data of the United States.
        """
        params = {
            'function': 'REAL_GDP_PER_CAPITA',
            'datatype': datatype
        }
        return self.call_api(params)

    def treasury_yield(self, interval='monthly', maturity='10year', datatype='json'):
        """
        TREASURY_YIELD function.
        This API returns the daily, weekly, and monthly US treasury yield of a given maturity timeline (e.g., 5 year, 30 year, etc).
        """
        params = {
            'function': 'TREASURY_YIELD',
            'interval': interval,
            'maturity': maturity,
            'datatype': datatype
        }
        return self.call_api(params)

    def federal_funds_rate(self, interval='monthly', datatype='json'):
        """
        FEDERAL_FUNDS_RATE function.
        This API returns the daily, weekly, and monthly federal funds rate (interest rate) of the United States.
        """
        params = {
            'function': 'FEDERAL_FUNDS_RATE',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def cpi(self, interval='monthly', datatype='json'):
        """
        CPI function.
        This API returns the monthly and semiannual consumer price index (CPI) of the United States. CPI is widely regarded as the barometer of inflation levels in the broader economy.
        """
        params = {
            'function': 'CPI',
            'interval': interval,
            'datatype': datatype
        }
        return self.call_api(params)

    def inflation(self, datatype='json'):
        """
        INFLATION function.
        This API returns the annual inflation rates (consumer prices) of the United States.
        """
        params = {
            'function': 'INFLATION',
            'datatype': datatype
        }
        return self.call_api(params)

    def retail_sales(self, datatype='json'):
        """
        RETAIL_SALES function.
        This API returns the monthly Advance Retail Sales: Retail Trade data of the United States.
        """
        params = {
            'function': 'RETAIL_SALES',
            'datatype': datatype
        }
        return self.call_api(params)

    def durables(self, datatype='json'):
        """
        DURABLES function.
        This API returns the monthly manufacturers' new orders of durable goods in the United States.
        """
        params = {
            'function': 'DURABLES',
            'datatype': datatype
        }
        return self.call_api(params)

    def unemployment(self, datatype='json'):
        """
        UNEMPLOYMENT function.
        This API returns the monthly unemployment rate of the United States.
        """
        params = {
            'function': 'UNEMPLOYMENT',
            'datatype': datatype
        }
        return self.call_api(params)

    def nonfarm_payroll(self, datatype='json'):
        """
        NONFARM_PAYROLL function.
        This API returns the monthly US All Employees: Total Nonfarm (commonly known as Total Nonfarm Payroll), a measure of the number of U.S. workers in the economy that excludes proprietors, private household employees, unpaid volunteers, farm employees, and the unincorporated self-employed.
        """
        params = {
            'function': 'NONFARM_PAYROLL',
            'datatype': datatype
        }
        return self.call_api(params)

    def sma(self, symbol, interval, time_period, series_type, datatype='json'):
        """
        SMA function.
        This API returns the simple moving average (SMA) values.
        """
        params = {
            'function': 'SMA',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': series_type,
            'datatype': datatype
        }
        return self.call_api(params)

    def ema(self, symbol, interval, time_period, series_type, datatype='json'):
        """
        EMA function.
        This API returns the exponential moving average (EMA) values.
        """
        params = {
            'function': 'EMA',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': series_type,
            'datatype': datatype
        }
        return self.call_api(params)

    def wma(self, symbol, interval, time_period, series_type, datatype='json'):
        """
        WMA function.
        This API returns the weighted moving average (WMA) values.
        """
        params = {
            'function': 'WMA',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': series_type,
            'datatype': datatype
        }
        return self.call_api(params)
