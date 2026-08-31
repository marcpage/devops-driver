#!/usr/bin/env python3

"""Module Doc"""

from types import SimpleNamespace
from dataclasses import dataclass, field

from devopsdriver.azdo.workitem.client import Client
from devopsdriver.azdo import Wiql, Equal
from azure.devops.exceptions import AzureDevOpsServiceError


class MockAzDoWorkItem:
    """Mocks a work item"""

    def __init__(self, id: int, **kwargs):
        self.id = id
        self.properties = kwargs

    def as_dict(self) -> dict:
        """Get the item as a dictionary"""
        return {"id": id, **self.properties}


class MockClient:  # pylint: disable=too-few-public-methods
    """fake an azure work item client, at least what we use"""

    def __init__(self):
        self.query = None

    def get_work_items(
        self, ids: list[int], expand: str | None = None
    ) -> list[MockAzDoWorkItem]:
        """mock out the get_work_items"""
        assert ids

        if 5 in ids:
            raise AzureDevOpsServiceError(
                SimpleNamespace(
                    inner_exception=None,
                    message="You do not have access to Work Item #5",
                    exception_id=5,
                    type_name="Type",
                    type_key="Key",
                    error_code=5,
                    event_id=5,
                    custom_properties=None,
                )
            )

        return [MockAzDoWorkItem(id=i) for i in ids]

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
    history = client.get_history(2)
    assert not history


def test_find() -> None:
    """Tests the find with the devops azure WorkItem"""
    client = Client(MockClient())
    found = client.find(Wiql().select("State").where(Equal("State", "New")))
    assert len(found) == 20


@dataclass
class WorkItem:  # pylint: disable=too-many-instance-attributes
    """A Work Item"""

    id: int = field(metadata={"lookup": "/id"})
    url: str = field(metadata={"lookup": "/url"})
    title: str = field(metadata={"lookup": "/fields/System.Title"})
    parent: int | None = field(
        metadata={
            "lookup": "/relations/(/attributes/name=Parent).first/url.split(/).last.int"
        }
    )
    children: list[int] = field(
        metadata={
            "lookup": "/relations/(/attributes/name=Child)/url.split(/).last.int",
            "default": [],
        }
    )


def test_fetch_work_items() -> None:
    """Tests fetch_work_items"""
    client = Client(MockClient())
    found = client.fetch_work_items(list(range(2005)), WorkItem)
    assert len(found) == 2004
    assert not any(i.id == 5 for i in found)


def test_fetch_work_items_bad_params() -> None:
    """Tests fetch_work_items"""
    client = Client(MockClient())

    try:
        found = client.fetch_work_items(list(range(2005)), WorkItem, batch_size=0)
        assert False, "Should have thrown"

    except ValueError:
        pass

    try:
        found = client.fetch_work_items(list(range(2005)), WorkItem, max_threads=0)
        assert False, "Should have thrown"

    except ValueError:
        pass

    found = client.fetch_work_items([], WorkItem)
    assert not found


if __name__ == "__main__":
    test_find()
    test_history()
    test_basic()
