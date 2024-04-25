#!/usr/bin/env python3


""" Azure Build Client """


from datetime import datetime
from azure.devops.v7_1.build import BuildClient

from .build import Build


class Client:
    def __init__(self, client: BuildClient):
        self.client = client

    def list(
        self,
        project: str,
        pipelines: list[int] = None,
        start: datetime = None,
        end: datetime = None,
        status: str = None,
        result: str = None,
        properties: list[str] = None,
        branch: str = None,
    ):
        continuation = None
        return [
            Build(self.client, b)
            for b in self.client.get_builds(
                project,
                continuation_token=continuation,
                definitions=pipelines,
                min_time=start,
                max_time=end,
                status_filter=status,
                result_filter=result,
                properties=properties,
                branch_name=branch,
            )
        ]
