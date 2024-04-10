#!/usr/bin/env python3

""" Pipeline client """

from azure.devops.v7_1.pipelines import PipelinesClient

from .pipeline import Pipeline


class PipelineClient:
    def __init__(self, client: PipelinesClient):
        self.client = client

    def list(self, project: str) -> list[Pipeline]:
        return [
            Pipeline(self.client, project, p)
            for p in self.client.list_pipelines(project)
        ]
