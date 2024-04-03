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
        return self.client.query_by_wiql(
            AzureWiql(query=str(wiql)),
            team_context=team_context,
            time_precision=time_precision,
            top=top,
        )

    def find(self, wiql: Wiql | str, top: int = None) -> list:
        if isinstance(wiql, Wiql):
            wiql.select("Id")

        found = self.query(wiql, top=top)
        print(found.as_dict())
