#!/usr/bin/env python3

""" Test build object """

from types import SimpleNamespace

from devopsdriver.azdo.builds.build import Build
from devopsdriver.azdo.azureobject import AzureObject


class MockTimeline:  # pylint: disable=too-few-public-methods
    """mock timeline"""

    def __init__(self, d: dict):
        self.d = d

    def as_dict(self) -> dict:
        """mock as_dict"""
        return self.d


class MockClient:
    """mock build client"""

    def get_build_log_lines(self, project, build_id, log_id) -> list[str]:
        """mock get_build_log_lines"""
        return [f"project={project}", f"build={build_id}", f"log={log_id}"]

    def get_build_timeline(self, project, build_id):
        """mock get_build_timeline"""
        return SimpleNamespace(
            records=[
                MockTimeline(
                    {
                        "parent_id": None,
                        "id": "5",
                        "project": project,
                        "build_id": build_id,
                        "log": {"id": 9},
                    }
                ),
                MockTimeline(
                    {
                        "parent_id": "5",
                        "id": "6",
                        "project": project,
                        "build_id": build_id,
                        "log": {"id": 6},
                    }
                ),
            ]
        )


class MockBuild(AzureObject):  # pylint: disable=too-few-public-methods
    """mock build client"""

    def __init__(self, d: dict):
        self.d = d
        super().__init__(self)

    def as_dict(self) -> dict:
        """mock as_dict"""
        return self.d


def test_basic() -> None:
    """test basic functionailty"""
    build = Build(MockClient(), MockBuild({"project": {"name": "project"}, "id": 12}))
    logs = build.get_logs().all_logs()
    assert len(logs) == 2, logs


def test_azure_object() -> None:
    """test string conversions for data objects"""
    build = MockBuild({"project": {"name": "project"}, "id": 12})
    assert (
        str(build)
        == """{
  "project": {
    "name": "project"
  },
  "id": 12
}"""
    ), str(build)
    assert (
        repr(build)
        == """{
  "project": {
    "name": "project"
  },
  "id": 12
}"""
    ), repr(build)


if __name__ == "__main__":
    test_basic()
    test_azure_object()
