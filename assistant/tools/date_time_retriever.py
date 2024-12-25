"""Current date and time tool spec"""

import datetime
from llama_index.core.tools.tool_spec.base import BaseToolSpec


class CurrentDateTimeToolSpec(BaseToolSpec):
    """Current date and time tool spec.

    """

    spec_functions = ["current_date_and_time"]

    def current_date_and_time(self) -> str:
        """
        A function that returns the current date and time.

        The time is in GMT format. it is currently not possible to convert to another timezone.

        """
        return f'Returns the current date is {datetime.datetime.now().strftime("%A, %B %d, %Y")}, and time {datetime.datetime.now().strftime("%H:%M:%S")}. tell the user that this is GMT.'
