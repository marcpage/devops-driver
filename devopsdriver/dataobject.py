#!/usr/bin/env python3

""" Data Objects """


class DataObject:  # pylint: disable=too-few-public-methods
    """dict like object with fuzzy field matching"""

    def __init__(self, data: dict):
        self.data = data

    def _matches_field(self, name: str, field: str) -> bool:
        name = name.lower()
        field = field.lower()

        if name == field:
            return True

        if name == field.replace(".", "_"):
            return True

        if name == field.split(".")[-1]:
            return True

        return False

    def _parse_value(self, data: any) -> any:
        if isinstance(data, dict):
            return DataObject._Dict(self, data)

        if isinstance(data, list):
            return [self._parse_value(d) for d in data]

        return data

    def _get_field(self, name: str, data: dict) -> any:
        assert name and data
        found = [f for f in data if self._matches_field(name, f)]
        assert len(found) in {0, 1}, found

        if len(found) == 1:
            return self._parse_value(data[found[0]])

        return None

    def __getattr__(self, name: str) -> any:
        return self._get_field(name, self.data)

    class _Dict(dict):
        def __init__(self, dataobject, data: dict):
            self.dataobject = dataobject
            super().__init__(data)

        def __getattr__(self, name: str) -> any:
            return self.dataobject._get_field(name, self)
