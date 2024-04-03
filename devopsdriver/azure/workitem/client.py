#!/usr/bin/env python3

""" Azure WorkItem Client """

from azure.devops.v7_1.work_item_tracking.models import Wiql as AzureWiql
from azure.devops.v7_1.work_item_tracking.models import TeamContext
from azure.devops.v7_1.work_item_tracking.models import WorkItemQueryResult
from devopsdriver.azure.workitem.wiql import Wiql


class Client:  # pylint: disable=too-few-public-methods
    """Wraps work item client"""

    def __init__(self, client):
        self.client = client

    def query(
        self,
        wiql: Wiql | str,
        team_context: TeamContext = None,
        time_precision: bool = None,
        top: int = None,
    ) -> WorkItemQueryResult:
        """Perform a wiql query

        Args:
            wiql (Wiql | str): The query
            team_context (TeamContext, optional): context object. Defaults to None.
            time_precision (bool, optional): True for precision time. Defaults to None.
            top (int, optional): Count of items to get. Defaults to None.

        Returns:
            WorkItemQueryResult: The results
        """
        return self.client.query_by_wiql(
            AzureWiql(query=str(wiql)),
            team_context=team_context,
            time_precision=time_precision,
            top=top,
        )

    def find_ids(self, wiql: Wiql | str, top: int = None) -> list:
        """Given a query, find the work item ids

        Args:
            wiql (Wiql | str): The query
            top (int, optional): The number of results to return. Defaults to None.

        Returns:
            list: List of item ids
        """
        if isinstance(wiql, Wiql):
            wiql.select("Id")

        found = self.query(wiql, top=top)
        # top-level items: as_of, columns, query_results_type, query_type, work_items
        # work_items fields: id, url
        # query_results_type: workItem
        # query_type: flat
        # columns: list of name, reference_name, url
        return [i.id for i in found.work_items]
