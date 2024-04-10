#!/usr/bin/env python3

""" Azure Pipeline """

from azure.devops.v7_1.pipelines.models import Pipeline as AzurePipeline
from azure.devops.v7_1.pipelines import PipelinesClient

from .run import Run


class Pipeline:
    """self.raw.fields
    "folder": "\\",
    "id": 1,
    "name": "DevOps",
    "revision": 1,
    "_links": {},
    "url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1?revision=1"
    """

    def __init__(self, client: PipelinesClient, project: str, pipeline: AzurePipeline):
        self.client = client
        self.project = project
        self.raw = pipeline

    def get_runs(self):
        return [
            Run(self.client, self.project, self.raw, r)
            for r in self.client.list_runs(self.project, self.raw.id)
        ]


""" pipeline
"folder": "\\",
"id": 1,
"name": "DevOps",
"revision": 1,
"_links": {},
"url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1?revision=1"
"""

""" run
"id": 1,
"name": "20240325.1",
"_links": {},
"created_date": "2024-03-25T23:53:38.503126Z",
"finished_date": "2024-03-25T23:53:43.467565Z",
"pipeline": {
    "folder": "\\",
    "id": 1,
    "name": "DevOps",
    "revision": 1,
    "url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1?revision=1"
},
"result": "failed",
"state": "completed",
"template_parameters": {},
"url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1/runs/1"
"""

""" log with expand=signedContent
"created_on": "2024-04-08T23:00:59.020Z",
"id": 8,
"last_changed_on": "2024-04-08T23:00:59.160Z",
"line_count": 4,
"signed_content": {
    "signature_expires": "2024-04-10T01:06:18.306299Z",
    "url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1/runs/10/signedlogcontent/8?urlExpires=2024-04-10T01%3A06%3A18.3062992Z&urlSigningMethod=HMACV1&urlSignature=2pv0SC3rVbDJwLdzNBUoCTfQc0VgPvndxkw2aB3g9iA%3D"
},
"url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1/runs/10/logs/8"
"""
