#!/usr/bin/env python3

""" Test Pipeline Client"""

from devopsdriver.azdo.pipeline.client import PipelineClient


class MockAzurePipeline:  # pylint: disable=too-few-public-methods
    """mock azure pipeline object"""

    def __init__(self, project: str):
        self.project = project

    def as_dict(self):
        """mock as_dict"""
        return {"project": self.project}


class MockAzurePipelinesClient:  # pylint: disable=too-few-public-methods
    """mock pipelines client"""

    def list_pipelines(self, project: str):
        """mock list_pipelines"""
        return [MockAzurePipeline(f"{project} 1"), MockAzurePipeline(f"{project} 2")]


def test_client() -> None:
    """tests the pipeline client"""
    client = PipelineClient(MockAzurePipelinesClient())
    pipelines = client.list("project")
    assert len(pipelines) == 2, pipelines


if __name__ == "__main__":
    test_client()
