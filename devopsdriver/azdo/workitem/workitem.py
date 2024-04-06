#!/usr/bin/env python3


""" An Azure Devops WorkItem """


from typing import Any

from azure.devops.v7_1.work_item_tracking.models import WorkItem as AzureWorkItem

from devopsdriver.azdo.timestamp import Timestamp


class WorkItem:  # pylint: disable=too-few-public-methods
    """Azure WorkItem"""

    def __init__(self, work_item: AzureWorkItem):
        self.raw = work_item

    @staticmethod
    def __matches_field(name: str, field: str) -> bool:
        name = name.lower()
        field = field.lower()

        if name == field:
            return True

        if name == field.replace(".", "_"):
            return True

        if name == field.split(".")[-1]:
            return True

        return False

    @staticmethod
    def _parse_field(name: str, data: dict) -> any:
        assert name and data
        found = [f for f in data if WorkItem.__matches_field(name, f)]

        if len(found) == 1:
            return (
                WorkItem._Dict(data[found[0]])
                if isinstance(data[found[0]], dict)
                else data[found[0]]
            )

        if "fields" in data:
            return WorkItem._parse_field(name, data["fields"])

        return None

    class _Dict(dict):
        def __getattr__(self, name: str) -> Any:
            value = WorkItem._parse_field(name, self)

            if Timestamp.is_timestamp(value):
                return Timestamp(value)

            return value

    def __getattr__(self, name: str) -> Any:
        value = WorkItem._parse_field(name, self.raw.as_dict())

        if Timestamp.is_timestamp(value):
            return Timestamp(value)

        return value
