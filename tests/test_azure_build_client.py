#!/usr/bin/env python3

""" Test azure build client """

from datetime import datetime

from devopsdriver.azdo.builds.client import Client


class MockObject:
    """mock object"""

    def __init__(self, d: dict):
        self.d = d

    def as_dict(self) -> dict:
        """mock as_dict

        Returns:
            dict: the dict
        """
        return self.d


class MockClient:
    """mock build client"""

    def get_builds(
        self,
        project,
        definitions,
        min_time,
        max_time,
        status_filter,
        result_filter,
        properties,
        branch_name,
        continuation_token=None,
    ):
        """mock get_builds"""
        return [
            MockObject(
                {
                    "project": project,
                    "pipelines": definitions,
                    "start": min_time,
                    "end": max_time,
                    "status": status_filter,
                    "result": result_filter,
                    "fields": properties,
                    "branch": branch_name,
                    "token": continuation_token,
                }
            )
        ]


def test_basic() -> None:
    """Test basic functionality"""
    client = Client(MockClient())
    results = client.list(
        "project",
        [1, 2, 3],
        datetime.now(),
        datetime.now(),
        "completed",
        "success",
        ["id"],
        "main",
    )
    assert len(results) == 1, results
    assert results[0].project == "project"


if __name__ == "__main__":
    test_basic()
