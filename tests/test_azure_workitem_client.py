#!/usr/bin/env python3

""" Module Doc """

from types import SimpleNamespace

from devopsdriver.azdo.workitem.client import Client
from devopsdriver.azdo import Wiql, Equal


class MockClient:  # pylint: disable=too-few-public-methods
    """fake an azure work item client, at least what we use"""

    def __init__(self):
        self.query = None

    def query_by_wiql(self, wiql, team_context, time_precision, top) -> SimpleNamespace:
        """mock out the query_by_wiql"""
        self.query = wiql.query
        assert team_context is None, team_context
        assert time_precision is None, time_precision
        assert top is None, top
        return SimpleNamespace(
            work_items=[SimpleNamespace(id=number) for number in range(0, 20)]
        )

    def get_revisions(self, wi_id, project, top, skip, expand):
        """Mock out get_revisions"""
        assert project is None, project
        assert top is None, top
        assert skip is None, skip
        assert expand is None, expand
        assert 0 <= wi_id < 20
        return []


def test_basic() -> None:
    """Perform basic test on search and find_ids"""
    client = Client(MockClient())
    ids = client.find_ids(Wiql().select("State").where(Equal("State", "New")))
    assert ids == list(range(0, 20))


def test_history() -> None:
    """test history"""
    client = Client(MockClient())
    history = client.history(2)
    assert not history


def test_find() -> None:
    """Tests the find with the devops azure WorkItem"""
    client = Client(MockClient())
    found = client.find(Wiql().select("State").where(Equal("State", "New")))
    assert len(found) == 20


if __name__ == "__main__":
    test_find()
    test_history()
    test_basic()
