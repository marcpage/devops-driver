#!/usr/bin/env python3


""" Azure Build Client """


from datetime import datetime
from azure.devops.v7_1.build import BuildClient

from .build import Build


class Client:  # pylint: disable=too-few-public-methods
    """The Build client"""

    def __init__(self, client: BuildClient):
        self.client = client

    def list(  # pylint: disable=too-many-positional-arguments
        self,
        project: str,
        pipelines: list[int] = None,
        start: datetime = None,
        end: datetime = None,
        status: str = None,
        result: str = None,
        properties: list[str] = None,
        branch: str = None,
    ) -> list[Build]:
        """Get the list of builds

        Args:
            project (str): The name of the project
            pipelines (list[int], optional): List of pipeline ids. Defaults to None.
            start (datetime, optional): Earliest time. Defaults to None.
            end (datetime, optional): Latest time. Defaults to None.
            status (str, optional): The status to get. Defaults to None.
            result (str, optional): The result to get. Defaults to None.
            properties (list[str], optional): List or properties to return. Defaults to None.
            branch (str, optional): The branch to search. Defaults to None.

        Returns:
            list[Build]: List of all the builds that match the given criteria
        """
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
