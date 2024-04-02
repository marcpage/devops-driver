#!/usr/bin/env python3


""" Establish a connection to Azure Devops 

API Documented here:
https://github.com/microsoft/azure-devops-python-api
"""

from azure.devops.connection import Connection as AzureConnection
from msrest.authentication import BasicAuthentication as MSBasicAuthentication

from devopsdriver.settings import Settings
from devopsdriver.azure.workitem.client import Client as WIClient

CONNECTION = AzureConnection
AUTHENTICATION = MSBasicAuthentication


class Azure:
    """A connection to Azure clients"""

    def __init__(
        self, settings: Settings = None, token: str = None, url: str = None, **clients
    ):
        settings = Settings(__file__) if settings is None else settings
        assert (token or "azure.token" in settings) and (
            url or "azure.url" in settings
        ), f"azure.token and azure.url not found in:\n{'\n'.join(settings.search_files)}"
        credentials = AUTHENTICATION("", Azure.__which(token, settings["azure.token"]))
        self.connection = CONNECTION(
            base_url=Azure.__which(url, settings["azure.url"]), creds=credentials
        )
        client_calls = {
            "workitem": self.connection.clients_v7_1.get_work_item_tracking_client
        }
        self.workitem = WIClient(Azure.__client("workitem", clients, client_calls))

    @staticmethod
    def __which(a: any, b: any) -> any:
        return b if a is None else a

    @staticmethod
    def __client(name: str, clients: dict, calls: dict) -> any:
        if clients and not clients.get(name, False):
            return None

        return calls[name]()
