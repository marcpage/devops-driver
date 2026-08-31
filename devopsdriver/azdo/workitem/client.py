#!/usr/bin/env python3


"""Azure WorkItem Client"""

from typing import TypeVar
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from azure.devops.v7_1.work_item_tracking.models import Wiql as AzureWiql
from azure.devops.v7_1.work_item_tracking.models import WorkItem as AzureWorkItem
from azure.devops.v7_1.work_item_tracking.models import TeamContext
from azure.devops.v7_1.work_item_tracking.models import WorkItemQueryResult
from azure.devops.exceptions import AzureDevOpsServiceError

from devopsdriver.azdo.azureobject import AzureObject
from devopsdriver.azdo.workitem.wiql import Wiql

T = TypeVar("T")


class Client:
    """Wraps work item client"""

    def __init__(self, client):
        self.client = client

    def query(
        self,
        wiql: Wiql | str,
        team_context: TeamContext | None = None,
        time_precision: bool | None = None,
        top: int | None = None,
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

    def _fetch_work_items_batch(
        self, ids: list[int], cls: type[T], expand: str | None = None
    ) -> list[T]:
        """Fetch a batch of work items, skipping deleted items."""

        if not ids:
            return []

        try:
            info_list = self.client.get_work_items(
                ids=ids,
                expand=expand,
            )

            return [AzureObject(info).convert_to(cls) for info in info_list]

        except AzureDevOpsServiceError:
            if len(ids) == 1:
                return []

        midpoint = len(ids) // 2
        first_half = self._fetch_work_items_batch(ids[:midpoint], cls, expand)
        return [
            *first_half,
            *self._fetch_work_items_batch(ids[midpoint:], cls, expand),
        ]

    def fetch_work_items(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        ids: list[int],
        cls: type[T],
        expand: str | None = None,
        batch_size: int = 200,
        max_threads: int = 8,
    ) -> list[T]:
        """Fetch work items in parallel batches, skipping deleted items."""
        if not ids:
            return []

        if batch_size <= 0:
            raise ValueError("batch_size must be greater than zero")

        if max_threads <= 0:
            raise ValueError("max_threads must be greater than zero")

        batches = [ids[i : i + batch_size] for i in range(0, len(ids), batch_size)]
        fetch_batch = partial(
            self._fetch_work_items_batch,
            cls=cls,
            expand=expand,
        )

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            results = executor.map(fetch_batch, batches)

        return [item for batch in results for item in batch]

    def get_history(  # pylint: disable=too-many-positional-arguments,too-many-arguments
        self,
        wi_id: int,
        project: str | None = None,
        top: int | None = None,
        skip: int | None = None,
        expand: str | None = None,
    ) -> list[AzureWorkItem]:
        """Simple wrapper around get_revisions"""
        return self.client.get_revisions(wi_id, project, top, skip, expand)

    def find_ids(self, wiql: Wiql | str, top: int | None = None) -> list[int]:
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
        return [i.id for i in found.work_items] if found.work_items else []

    def find(self, wiql: Wiql | str, top: int | None = None) -> list[list[AzureObject]]:
        """Gets the full history of items found in a WIQL search

        Args:
            wiql (Wiql | str): The query
            top (int, optional): The number of work items to return. Defaults to None.

        Returns:
            list[list[WorkItem]]: List of work items, each is a history of work items
        """
        return [
            [AzureObject(e) for e in self.get_history(i)]
            for i in self.find_ids(wiql, top)
        ]
