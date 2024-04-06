#!/usr/bin/env python3


""" Azure WorkItem Client """


from azure.devops.v7_1.work_item_tracking.models import Wiql as AzureWiql
from azure.devops.v7_1.work_item_tracking.models import WorkItem as AzureWorkItem
from azure.devops.v7_1.work_item_tracking.models import TeamContext
from azure.devops.v7_1.work_item_tracking.models import WorkItemQueryResult
from devopsdriver.azdo.workitem.workitem import WorkItem
from devopsdriver.azdo.workitem.wiql import Wiql


class Client:
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

    def history(  # pylint: disable=too-many-arguments
        self,
        wi_id: int,
        project: str = None,
        top: int = None,
        skip: int = None,
        expand: str = None,
    ) -> list[AzureWorkItem]:
        """Simple wrapper around get_revisions"""
        return self.client.get_revisions(wi_id, project, top, skip, expand)

    def find_ids(self, wiql: Wiql | str, top: int = None) -> list[int]:
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

    def find(self, wiql: Wiql | str, top: int = None) -> list[list[WorkItem]]:
        """Gets the full history of items found in a WIQL search

        Args:
            wiql (Wiql | str): The query
            top (int, optional): The number of work items to return. Defaults to None.

        Returns:
            list[list[WorkItem]]: List of work items, each is a history of work items
        """
        return [
            [WorkItem(e) for e in self.history(i)] for i in self.find_ids(wiql, top)
        ]
