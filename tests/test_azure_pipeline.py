#!/usr/bin/env python3

""" Test Pipeline """

from devopsdriver.azdo.pipeline.pipeline import Pipeline


class MockRun:  # pylint: disable=too-few-public-methods
    """moc out a run"""

    def __init__(self, value: str):
        self.value = value

    def as_dict(self):
        """mock out list_runs method"""
        return {"id": self.value}


class MockPipelineClient:
    """mock pipeline client"""

    def as_dict(self):
        """mock out as_dict method"""
        return {}

    def list_runs(self, project: str, pipeline_id: int):
        """mock out list_runs method"""
        return [MockRun(project), MockRun(pipeline_id)]


class MockPipeline:  # pylint: disable=too-few-public-methods
    """mock out Azure pipeline object"""

    def as_dict(self):
        """mock out list_runs method"""
        return {"id": 5}


def test_pipeline() -> None:
    """tests basic pipeline functionality"""
    pipeline = Pipeline(MockPipelineClient(), "project", MockPipeline())
    runs = pipeline.get_runs()
    assert len(runs) == 2, runs


if __name__ == "__main__":
    test_pipeline()
