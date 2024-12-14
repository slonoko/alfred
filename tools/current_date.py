"""
title: String Inverse
author: Your Name
author_url: https://website.com
git_url: https://github.com/username/string-reverse.git
description: This tool calculates the inverse of a string
required_open_webui_version: 0.4.0
requirements: llama-index,llama-index-core
version: 0.4.0
licence: MIT
"""
import datetime
from pydantic import BaseModel, Field

class Tools:
    def __init__(self):
        """Initialize the Tool."""
        pass

    class Valves(BaseModel):
        pass

    def current_date(self) -> str:
        """
        Retrieves the current date and time
        """
        return f'Provide the current date which is {datetime.datetime.now().strftime("%A, %B %d, %Y")}, and the current time which is {datetime.datetime.now().strftime("%H:%M:%S")}. make sure to mention that the time is in GMT format'