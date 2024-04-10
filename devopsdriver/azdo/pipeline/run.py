#!/usr/bin/env python3

""" Pipeline Run """

from azure.devops.v7_1.pipelines.models import Pipeline
from azure.devops.v7_1.pipelines.models import Run as AzureRun
from azure.devops.v7_1.pipelines import PipelinesClient

from devopsdriver.azdo import AzureObject

from .log import Log


class Run(AzureObject):  # pylint: disable=too-few-public-methods
    """Run fields:
    id (1)
    name ("20240325.1")
    _links ({})
    created_date ("2024-03-25T23:53:38.503126Z")
    finished_date ("2024-03-25T23:53:43.467565Z")
    pipeline (see Pipeline)
    result ("failed")
    state ("completed")
    template_parameters ({})
    url ("https://dev.azure.com/Org/<guid>/_apis/pipelines/1/runs/1")
    """

    def __init__(
        self, client: PipelinesClient, project: str, pipeline: Pipeline, run: AzureRun
    ):
        self.client = client
        self.project = project
        self.pipeline = pipeline
        super().__init__(run)

    def logs(self):
        """Get Logs for the run"""
        return [
            Log(l)
            for l in self.client.list_logs(
                self.project, self.pipeline.id, self.raw.id, expand="signedContent"
            )
        ]
