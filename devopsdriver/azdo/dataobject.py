#!/usr/bin/env python3


""" An Azure Devops WorkItem """


from azure.devops.v7_1.work_item_tracking.models import WorkItem as AzureWorkItem

from devopsdriver.azdo.timestamp import Timestamp
from devopsdriver.dataobject import DataObject as GenericDataObject


class DataObject(GenericDataObject):  # pylint: disable=too-few-public-methods
    """Azure WorkItem"""

    def __init__(self, work_item: AzureWorkItem):
        self.raw = work_item
        super().__init__(self.raw.as_dict())

    def _parse_value(self, data: any) -> any:
        if isinstance(data, str) and Timestamp.is_timestamp(data):
            return Timestamp(data)

        return super()._parse_value(data)

    def _get_field(self, name: str, data: dict) -> any:
        value = super()._get_field(name, data)

        if value is None and "fields" in data:
            return self._get_field(name, data["fields"])

        return value
