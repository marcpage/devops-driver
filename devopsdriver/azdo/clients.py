#!/usr/bin/env python3


""" Establish a connection to Azure Devops 

API Documented here:
https://github.com/microsoft/azure-devops-python-api
"""


from azure.devops.connection import Connection as AzureConnection
from msrest.authentication import BasicAuthentication as MSBasicAuthentication

from devopsdriver.settings import Settings
from devopsdriver.azdo.workitem.client import Client as WIClient
from devopsdriver.azdo.pipeline.client import Client as PLClient


# for testing
CONNECTION = AzureConnection
AUTHENTICATION = MSBasicAuthentication


class Azure:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """A connection to Azure clients"""

    def __init__(
        self, settings: Settings = None, token: str = None, url: str = None, **clients
    ):
        settings = (
            Settings(__file__).key("secrets")
            if settings is None and token is None and url is None
            else settings
        )
        assert (token or "azure.token" in settings) and (
            url or "azure.url" in settings
        ), "azure.token and azure.url not found in:\n" + "\n".join(
            settings.search_files
        )
        url = settings["azure.url"] if url is None else url
        token = settings["azure.token"] if token is None else token
        self.connection = CONNECTION(base_url=url, creds=AUTHENTICATION("", token))
        client_calls = {
            "workitem": self.connection.clients_v7_1.get_work_item_tracking_client,
            "pipeline": self.connection.clients_v7_1.get_pipelines_client,
            "task": self.connection.clients_v7_1.get_task_agent_client,
            "git": self.connection.clients_v7_1.get_git_client,
            "core": self.connection.clients_v7_1.get_core_client,
            "build": self.connection.clients_v7_1.get_build_client,
            "identity": self.connection.clients_v7_1.get_identity_client,
        }
        unsupported_clients = set(clients) - set(client_calls)
        assert not unsupported_clients, f"{unsupported_clients} not supported"
        self.workitem = WIClient(Azure.__client("workitem", clients, client_calls))
        self.pipeline = PLClient(Azure.__client("pipeline", clients, client_calls))
        self.core = Azure.__client("core", clients, client_calls)
        self.task = Azure.__client("task", clients, client_calls)
        self.git = Azure.__client("git", clients, client_calls)
        self.build = Azure.__client("build", clients, client_calls)
        self.identity = Azure.__client("identity", clients, client_calls)

    @staticmethod
    def __client(name: str, clients: dict, calls: dict) -> any:
        if clients and not clients.get(name, False):
            return None

        return calls[name]()
