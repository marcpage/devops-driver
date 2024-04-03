#!/usr/bin/env python3

""" Module Doc """

from devopsdriver.azure.workitem.client import Client
from devopsdriver.azure.clients import Azure


class FakeClient:
    pass


def test_basic() -> None:
    Azure().workitem.find(
        "SELECT [System.Id] FROM worktiem WHERE [System.CreatedDate] < @today"
    )


if __name__ == "__main__":
    test_basic()
