#!/usr/bin/env python3

""" Pipeline Run """

from azure.devops.v7_1.pipelines.models import Pipeline
from azure.devops.v7_1.pipelines.models import Run as AzureRun
from azure.devops.v7_1.pipelines import PipelinesClient

from .log import Log


class Run:
    def __init__(
        self, client: PipelinesClient, project: str, pipeline: Pipeline, run: AzureRun
    ):
        self.client = client
        self.project = project
        self.pipeline = pipeline
        self.run = run

    def logs(self):
        return [
            Log(self.client, self.project, self.pipeline, self.run, l)
            for l in self.client.list_logs(
                self.project, self.pipeline.id, self.run.id, expand="signedContent"
            )
        ]
