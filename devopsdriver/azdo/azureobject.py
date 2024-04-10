#!/usr/bin/env python3


""" An Azure Devops WorkItem """


from msrest.serialization import Model

from devopsdriver.azdo.timestamp import Timestamp
from devopsdriver.dataobject import DataObject


class AzureObject(DataObject):  # pylint: disable=too-few-public-methods
    """Azure WorkItem"""

    def __init__(self, azure_object: Model):
        self.raw = azure_object
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
