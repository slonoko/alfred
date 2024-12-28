"""Current date and time tool spec"""

import datetime
from llama_index.core.tools.tool_spec.base import BaseToolSpec
from zoneinfo import ZoneInfo
from pydantic import BaseModel

class CurrentDateTimeToolSpec(BaseToolSpec):
    """Current date and time tool spec.

    """

    spec_functions = ["current_date_and_time"]

    def current_date_and_time(self, format:str="%A, %B %d, %Y %H:%M:%S", timezone: str="localtime") -> str:
        """
        A usefull function that takes as input the date and time format as optional parameter, the timezone with default to the system locale, and returns the current date and time.
        """
        tz=ZoneInfo(timezone)
        return datetime.datetime.now(tz).strftime(format)

class DatetimeToolFnSchema(BaseModel):
    """Default tool function Schema."""

    format: str
    timezone: str