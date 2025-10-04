#!/usr/bin/env python3


"""test azure client logic"""


from tempfile import TemporaryDirectory
from types import SimpleNamespace
from os.path import join

from helpers import setup_settings, write

from devopsdriver.azdo import Azure
from devopsdriver.azdo import clients


class MockConnection:  # pylint: disable=too-few-public-methods
    """Fakes an Azure connection"""

    def __init__(self, base_url: str, creds: SimpleNamespace):
        self.base_url = base_url
        self.creds = creds

        class Clients71:  # pylint: disable=too-few-public-methods
            """Fakes a 7.1 clients factory"""

            SUPPORTED = {
                "get_work_item_tracking_client",
                "get_pipelines_client",
                "get_task_agent_client",
                "get_git_client",
                "get_core_client",
                "get_build_client",
                "get_identity_client",
                "get_graph_client",
            }

            def __getattr__(self, name: str) -> str:
                assert name in Clients71.SUPPORTED, name

                def function():
                    return name.replace("get_", "")

                return function

        self.clients_v7_1 = Clients71()


def test_basic() -> None:
    """test the basic calling"""
    clients.CONNECTION = MockConnection
    clients.AUTHENTICATION = lambda a, b: SimpleNamespace(empty=a, token=b)
    azure = Azure(None, "token", "https://url.com/project")
    assert (
        azure.connection.base_url == "https://url.com/project"
    ), azure.connection.base_url
    assert azure.connection.creds.token == "token", azure.connection.creds.token
    assert azure.connection.creds.empty == "", azure.connection.creds.empty
    assert azure.workitem.client == "work_item_tracking_client"


def test_settings() -> None:
    """test the basic calling"""
    clients.CONNECTION = MockConnection
    clients.AUTHENTICATION = lambda a, b: SimpleNamespace(empty=a, token=b)
    azure = Azure({"azure.token": "token", "azure.url": "https://url.com/project"})
    assert (
        azure.connection.base_url == "https://url.com/project"
    ), azure.connection.base_url
    assert azure.connection.creds.token == "token", azure.connection.creds.token
    assert azure.connection.creds.empty == "", azure.connection.creds.empty
    assert azure.workitem.client == "work_item_tracking_client"


def test_mixed_settings() -> None:
    """test the basic calling"""
    clients.CONNECTION = MockConnection
    clients.AUTHENTICATION = lambda a, b: SimpleNamespace(empty=a, token=b)
    azure = Azure(
        {"azure.token": "token", "azure.url": "https://url.com/project"},
        token="fake token",
    )
    assert (
        azure.connection.base_url == "https://url.com/project"
    ), azure.connection.base_url
    assert azure.connection.creds.token == "fake token", azure.connection.creds.token
    assert azure.connection.creds.empty == "", azure.connection.creds.empty
    assert azure.workitem.client == "work_item_tracking_client"

    azure = Azure(
        {"azure.token": "token", "azure.url": "https://url.com/project"},
        url="https://fake.com/project",
    )
    assert (
        azure.connection.base_url == "https://fake.com/project"
    ), azure.connection.base_url
    assert azure.connection.creds.token == "token", azure.connection.creds.token
    assert azure.connection.creds.empty == "", azure.connection.creds.empty
    assert azure.workitem.client == "work_item_tracking_client"

    azure = Azure(
        {"azure.token": "token", "azure.url": "https://url.com/project"},
        token="fake token",
        url="https://fake.com/project",
    )
    assert (
        azure.connection.base_url == "https://fake.com/project"
    ), azure.connection.base_url
    assert azure.connection.creds.token == "fake token", azure.connection.creds.token
    assert azure.connection.creds.empty == "", azure.connection.creds.empty
    assert azure.workitem.client == "work_item_tracking_client"


def test_load_settings() -> None:
    """test the basic calling"""
    with TemporaryDirectory() as working_dir:
        base_dir = join(working_dir, "base")
        setup_settings(
            os="Linux",
            shared="test",
            Linux=join(base_dir, "Linux"),
            Darwin=join(base_dir, "macOS"),
            Windows=join(base_dir, "Windows"),
        )
        write(
            join(base_dir, "Linux", "test.yml"),
            azure={"token": "token", "url": "https://url.com/project"},
        )
        clients.CONNECTION = MockConnection
        clients.AUTHENTICATION = lambda a, b: SimpleNamespace(empty=a, token=b)

        azure = Azure()
        assert (
            azure.connection.base_url == "https://url.com/project"
        ), azure.connection.base_url
        assert azure.connection.creds.token == "token", azure.connection.creds.token
        assert azure.connection.creds.empty == "", azure.connection.creds.empty
        assert (
            azure.workitem.client == "work_item_tracking_client"
        ), azure.workitem.client


def test_not_all_clients() -> None:
    """test the basic calling"""
    clients.CONNECTION = MockConnection
    clients.AUTHENTICATION = lambda a, b: SimpleNamespace(empty=a, token=b)
    azure = Azure(None, "token", "https://url.com/project", pipeline=True)
    assert (
        azure.connection.base_url == "https://url.com/project"
    ), azure.connection.base_url
    assert azure.connection.creds.token == "token", azure.connection.creds.token
    assert azure.connection.creds.empty == "", azure.connection.creds.empty
    assert azure.workitem.client is None


def test_unsupported_client() -> None:
    """test the basic calling"""
    clients.CONNECTION = MockConnection
    clients.AUTHENTICATION = lambda a, b: SimpleNamespace(empty=a, token=b)
    try:
        _ = Azure(None, "token", "https://url.com/project", google=True)
        raise KeyError("google should not have worked")

    except AssertionError as error:
        assert "google" in str(error), error


if __name__ == "__main__":
    test_unsupported_client()
    test_not_all_clients()
    test_load_settings()
    test_mixed_settings()
    test_settings()
    test_basic()
