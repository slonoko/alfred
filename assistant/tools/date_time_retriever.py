"""Current date and time tool spec"""

import datetime
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from zoneinfo import ZoneInfo

class CurrentDateTimeToolSpec(BaseToolSpec):
    """Current date and time tool spec.

    """

    spec_functions = ["current_date", "current_time"]

    def current_date(self, format:str="%A, %B %d, %Y", timezone: str="localtime") -> str:
        """
        A usefull function that takes as input the date format as optional parameter, the timezone with default to the system locale, and returns the current date.
        """
        tz=ZoneInfo(timezone)
        return datetime.datetime.now(tz).strftime(format)

    def current_time(self, format:str="%H:%M:%S", timezone: str="localtime") -> str:
        """
        A usefull function that takes as input the time format as optional parameter, the timezone with default to the system locale, and returns the time in the GMT timezone.
        """
        tz=ZoneInfo(timezone)
        return datetime.datetime.now(tz).strftime(format)
