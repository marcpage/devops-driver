#!/usr/bin/env python3


""" Pipeline client """


from azure.devops.v7_1.pipelines import PipelinesClient

from .pipeline import Pipeline


class PipelineClient:  # pylint: disable=too-few-public-methods
    """Pipeline Client wrapper"""

    def __init__(self, client: PipelinesClient):
        self.client = client

    def list(self, project: str) -> list[Pipeline]:
        """List the pipelines

        Args:
            project (str): The project to list

        Returns:
            list[Pipeline]: The list of pipeline objects
        """
        return [
            Pipeline(self.client, project, p)
            for p in self.client.list_pipelines(project)
        ]
