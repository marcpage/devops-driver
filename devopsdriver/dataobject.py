#!/usr/bin/env python3

"""Data Objects"""

from json import dumps
from re import fullmatch
from typing import Any


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

    def _parse_value(self, data: Any) -> Any:
        if isinstance(data, dict):
            return DataObject._Dict(self, data)

        if isinstance(data, list):
            return [self._parse_value(d) for d in data]

        return data

    def _get_field(self, name: str, data: dict) -> Any:
        assert name and data, f"name = {name} data = {data}"
        found = [f for f in data if self._matches_field(name, f)]
        assert len(found) in {0, 1}, found

        if len(found) == 1:
            return self._parse_value(data[found[0]])

        return None

    def __getattr__(self, name: str) -> Any:
        return self._get_field(name, self.data)

    def __str__(self) -> str:
        return dumps(self.data, indent=2)

    def __repr__(self) -> str:
        return dumps(self.data, indent=2)

    def lookup(self, path: str, default: Any = None) -> Any:
        """
        Resolves a custom path expression against the underlying data.

        Supported syntax:
            /key/subkey
            .first
            .last
            .split(delimiter)
            /(path=value)

        Examples:
            /id
            /fields/System.Title
            /relations/(/attributes/name=Parent).first/url.split(/).last
            /relations/(/attributes/name=Child)/url.split(/).last
        """

        tokens = self._tokenize(path)
        current = self.data

        try:
            for token in tokens:
                current = self._apply_token(current, token)

        except KeyError:
            return default

        return current

    def _tokenize(self, path: str) -> list[str]:
        """Splits a path into tokens while respecting parentheses."""

        path = path.strip("/")

        tokens: list[str] = []
        current: list[str] = []
        depth = 0

        for char in path:
            if char == "/" and depth == 0:
                if current:
                    tokens.append("".join(current))
                    current = []

                continue

            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1

            current.append(char)

        if current:
            tokens.append("".join(current))

        return tokens

    def _apply_token(self, value: Any, token: str) -> Any:
        """
        Applies a token to the current value.

        Supports chained expressions like:
            (...).first
            url.split(/).last.int
        But maintains tokens like:
            System.Title
        """
        segments = token.split(".")
        parts = []

        while segments[-1] in ("first", "last", "int") or segments[-1].startswith(
            "split"
        ):
            parts.insert(0, segments.pop())

        parts.insert(0, ".".join(segments))
        current = value
        group = False

        for part in parts:
            current, group = self._apply_part(current, part, group)

        return current

    def _apply_part(  # pylint: disable=too-many-return-statements
        self, value: Any, part: str, group: bool = False
    ) -> tuple[Any, bool]:
        """Applies a single operation."""
        if value is None:
            return None, group

        if part.startswith("(") and part.endswith(")"):  # List filter
            return self._filter_list(value, part[1:-1]), group

        if part == "first":  # first
            if not value:
                return None, group

            if group:
                return [v[0] for v in value], group

            return value[0], False

        if part == "last":  # last
            if not value:
                return None, group

            if group:
                return [v[-1] for v in value], group

            return value[-1], False

        if part == "int":  # int
            if group:
                return [int(v) for v in value], group

            return int(value), group

        # split(delimiter)
        split_only_match = fullmatch(r"split\((.*?)\)", part)

        if split_only_match:
            delimiter = split_only_match.group(1)

            if isinstance(value, list):
                return [item.split(delimiter) for item in value], group

            return value.split(delimiter), group

        if isinstance(value, dict):  # Dictionary lookup
            return value[part], group

        if isinstance(value, list):  # Apply lookup to all items in a list
            return [self._apply_part(item, part)[0] for item in value], True

        raise ValueError(f"Cannot apply '{part}' to value: {value}")

    def _filter_list(self, items: list[dict], expression: str) -> list[Any]:
        """
        Filters a list using an expression.

        Expression format:
            /path=value

        Example:
            /attributes/name=Parent
        """

        path_expr, expected = expression.split("=", 1)

        result = []

        for item in items:
            actual = DataObject(item).lookup(path_expr)

            if str(actual) == expected:
                result.append(item)

        return result

    class _Dict(dict):
        def __init__(self, dataobject, data: dict):
            self.dataobject = dataobject
            super().__init__(data)

        def __getattr__(self, name: str) -> Any:
            return self.dataobject._get_field(name, self)
