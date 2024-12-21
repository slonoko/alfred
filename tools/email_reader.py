"""
title: String Inverse
author: Your Name
author_url: https://website.com
git_url: https://github.com/username/string-reverse.git
description: This tool calculates the inverse of a string
required_open_webui_version: 0.4.0
requirements: llama-index,chromadb,llama-index-vector-stores-chroma,llama-index-core,llama-index-llms-ollama,llama-index-embeddings-huggingface
version: 0.4.0
licence: MIT
"""

from typing import List, Union, Generator, Iterator
import datetime
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.ollama import Ollama
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.tools import QueryEngineTool, ToolMetadata
import logging
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.base.response.schema import Response, StreamingResponse
from llama_index.core.schema import Document
from pydantic import BaseModel, Field
import base64
import email
from typing import Any, List, Optional

from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from pydantic import BaseModel
import logging
from tqdm import tqdm


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/gmail.compose",]


class GmailReader(BaseReader, BaseModel):
    """Gmail reader.

    Reads emails

    Args:
        max_results (Optional[int]): Defaults to None.
        query (str): Gmail query. Defaults to None.
        service (Any): Gmail service. Defaults to None.
        results_per_page (Optional[int]): Max number of results per page. Defaults to 10.
        use_iterative_parser (bool): Use iterative parser. Defaults to False.
    """

    query: str = None
    use_iterative_parser: bool = False
    service: Any = None
    max_results: Optional[int] = None
    results_per_page: Optional[int] = None

    def load_data(self) -> List[Document]:
        """Load emails from the user's account"""
        from googleapiclient.discovery import build

        credentials = self._get_credentials()
        if not self.service:
            self.service = build("gmail", "v1", credentials=credentials)

        messsages = self.search_messages()

        results = []
        for message in messsages:
            text = message.pop("body")
            extra_info = message
            document = Document(text=text, extra_info=extra_info or {})
            document.metadata = extra_info or {}
            results.append(document)

        return results

    def _get_credentials(self) -> Any:
        """Get valid user credentials from storage.

        The file token.json stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.

        Returns:
            Credentials, the obtained credential.
        """
        import os

        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow

        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    def search_messages(self):
        query = self.query

        max_results = self.max_results
        if self.results_per_page:
            max_results = self.results_per_page

        if(max_results):
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=int(max_results))
                .execute()
            )
            messages = results.get("messages", [])

            if len(messages) < self.max_results:
                # paginate if there are more results
                while "nextPageToken" in results:
                    page_token = results["nextPageToken"]
                    results = (
                        self.service.users()
                        .messages()
                        .list(
                            userId="me",
                            q=query,
                            pageToken=page_token,
                            maxResults=int(max_results),
                        )
                        .execute()
                    )
                    messages.extend(results["messages"])
                    if len(messages) >= self.max_results:
                        break
        else:
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query)
                .execute()
            )
            messages = results.get("messages", [])

            while "nextPageToken" in results:
                page_token = results["nextPageToken"]
                results = (
                    self.service.users()
                    .messages()
                    .list(
                        userId="me",
                        q=query,
                        pageToken=page_token
                    )
                    .execute()
                )
                messages.extend(results["messages"])



        result = []
        logging.info(f"Total number of messages found {len(messages)}")
        for i in tqdm(range(len(messages))):
            message = messages[i]
            try:
                message_data = self.get_message_data(message)
                if not message_data:
                    continue
                result.append(message_data)
            except Exception as e:
                #logging.error(msg=f"Can't get message data {str(e)}, for message with id {message['id']}")
                continue

        return result

    def get_message_data(self, message):
        message_id = message["id"]
        message_data = (
            self.service.users()
            .messages()
            .get(format="raw", userId="me", id=message_id)
            .execute()
        )
        if self.use_iterative_parser:
            body = self.extract_message_body_iterative(message_data)
        else:
            body = self.extract_message_body(message_data)

        if not body:
            return None

        # https://developers.google.com/gmail/api/reference/rest/v1/users.messages
        return {
            "id": message_data["id"],
            "threadId": message_data["threadId"],
            "snippet": message_data["snippet"],
            "internalDate": message_data["internalDate"],
            "body": body,
        }

    def extract_message_body_iterative(self, message: dict):
        if message["raw"]:
            body = base64.urlsafe_b64decode(message["raw"])
            mime_msg = email.message_from_bytes(body)
        else:
            mime_msg = message

        body_text = ""
        if mime_msg.get_content_type() == "text/plain":
            plain_text = mime_msg.get_payload(decode=True)
            charset = mime_msg.get_content_charset("utf-8")
            body_text = plain_text.decode(charset)

        elif mime_msg.get_content_maintype() == "multipart":
            msg_parts = mime_msg.get_payload()
            for msg_part in msg_parts:
                body_text += self.extract_message_body_iterative(msg_part)

        return body_text

    def extract_message_body(self, message: dict):
        from bs4 import BeautifulSoup

        try:
            body = base64.urlsafe_b64decode(message["raw"])
            mime_msg = email.message_from_bytes(body)

            # If the message body contains HTML, parse it with BeautifulSoup
            if "text/html" in mime_msg:
                soup = BeautifulSoup(body, "html.parser")
                body = soup.get_text()
            return body.decode("utf-8")
        except Exception as e:
            print("failed")
            raise Exception("Can't parse message body" + str(e))
class Tools:
    def __init__(self):
        """Initialize the Tool."""
        self.documents = None
        self.index = None
        self.valves = self.Valves()
        self.gmail_reader = GmailReader(use_iterative_parser=False)

    class Valves(BaseModel):
        GMAIL_CREDENTIALS: str = Field(
            default="",
            description="The Gmail API credentials",
        )

    def query_email(self, query: str) -> str:
        """
        search in the email database
        :param query: the text to use to query the email database
        """
        self.gmail_reader.query = query
        emails = self.gmail_reader.load_data()
        return ""