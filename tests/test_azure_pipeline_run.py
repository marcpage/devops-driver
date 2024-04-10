#!/usr/bin/env python3

""" Test pipeline run """

from types import SimpleNamespace

from devopsdriver.azdo.pipeline.run import Run
from devopsdriver.azdo.pipeline import log


class MockAzureRun:  # pylint: disable=too-few-public-methods
    """Mock azure run object"""

    def __init__(self, run_id):
        self.id = run_id

    def as_dict(self):
        """mock as_dict"""
        return {"id": 48}


class MockLog:  # pylint: disable=too-few-public-methods
    """mock azure log object"""

    def __init__(self, text):
        self.text = text
        self.signed_content = SimpleNamespace(url=SimpleNamespace(text="some dumb url"))

    def as_dict(self):
        """mock as_dict"""
        return {"id": 22}


class MockPipelineClient:  # pylint: disable=too-few-public-methods
    """mock azure pipelines client"""

    def __init__(self):
        self.project = None
        self.pipeline_id = None
        self.run_id = None
        self.expand = None

    def list_logs(self, project, pipeline_id, run_id, expand):
        """mock list_logs"""
        self.project = project
        self.pipeline_id = pipeline_id
        self.run_id = run_id
        self.expand = expand
        return [MockLog("log 1"), MockLog("log 2")]


class MockPipeline:  # pylint: disable=too-few-public-methods
    """mock pipeline object"""

    def __init__(self, pipeline_id):
        self.id = pipeline_id


def test_basic() -> None:
    """test basic run and log"""
    log.GET_URL = lambda x, timeout: x
    run = Run(MockPipelineClient(), "project", MockPipeline(5), MockAzureRun(83))
    logs = run.logs()
    assert len(logs) == 2, logs


if __name__ == "__main__":
    test_basic()
