#!/usr/bin/env python3


"""Azure Pipeline"""


from azure.devops.v7_1.pipelines.models import Pipeline as AzurePipeline
from azure.devops.v7_1.pipelines import PipelinesClient

from devopsdriver.azdo import AzureObject

from .run import Run


class Pipeline(AzureObject):  # pylint: disable=too-few-public-methods
    """Pipeline fields:
    folder ("\\")
    id (1)
    name (DevOps)
    revision (1),
    _links ({}),
    url (https://dev.azure.com/Org/<guid>/_apis/pipelines/1?revision=1)
    """

    def __init__(self, client: PipelinesClient, project: str, pipeline: AzurePipeline):
        self.client = client
        self.project = project
        super().__init__(pipeline)

    def get_runs(self):
        """Gets the top 10,000 runs for this pipeline"""
        return [
            Run(self.client, self.project, self.raw, r)
            for r in self.client.list_runs(self.project, self.id)
        ]
