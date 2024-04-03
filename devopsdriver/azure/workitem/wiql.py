#!/usr/bin/env python3

""" Builds a WIQL query
https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax?view=azure-devops

SELECT
    [System.Id],
    [System.AssignedTo],
    [System.State],
    [System.Title],
    [System.Tags]
FROM workitems
WHERE
    [System.TeamProject] = 'Design Agile'
    AND [System.WorkItemType] = 'User Story'
    AND [System.State] = 'Active'
ORDER BY [System.ChangedDate] DESC
ASOF '02-11-2020'
"""


from datetime import datetime, date


class Field:  # pylint disable=too-few-public-methods
    """column name"""

    SYSTEM = {
        "Id",
        "AssignTo",
        "State",
        "Title",
        "Tags",
        "TeamProject",
        "WorkItemType",
        "ChangedDate",
    }

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return f"[{'System.' if self.value in Field.SYSTEM else ''}{self.value}]"


class OrderBy:  # pylint disable=too-few-public-methods
    """Order by field"""

    def __init__(self, field: Field, order: str = "DESC"):
        self.field = field
        self.order = order

    def __str__(self) -> str:
        return f"{self.field} {self.order}"


class Ascending:  # pylint disable=too-few-public-methods
    """Order by field ascending"""

    def __init__(self, field: Field):
        self.field = field
        super().__init__(field, "ASC")


class Descending:  # pylint disable=too-few-public-methods
    """Order by field descending"""

    def __init__(self, field: Field):
        self.field = field
        super().__init__(field, "DESC")


class Value:  # pylint disable=too-few-public-methods
    """A constant value"""

    def __init__(self, value: any):
        self.value = value

    def __str__(self) -> str:
        if isinstance(self.value, datetime):
            return self.value.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(self.value, date):
            return self.value.strftime("%Y-%m-%d")

        if isinstance(self.value, int):
            return str(self.value)

        if isinstance(self.value, float):
            return f"{self.value:0.3f}"

        if isinstance(self.value, str):
            return f'"{self.value}"'  # TODO: escape value  # pylint: disable=fixme


class Builder:
    """Build a WIQL query"""

    def __init__(self):
        self.selected = [Field("Id")]
        self.search = None
        self.order = []
        self.snapshot = None

    def order_by(self, *orders):
        """Set the fields to order the results by

        Returns:
            Builder: Returns self for chaining
        """
        self.order = orders
        return self

    def select(self, *fields):
        """The fields to select

        Returns:
            Builder: Returns self for chaining
        """
        self.selected = fields
        return self

    def asof(self, date: Value):
        """Set the view of the data

        Args:
            date (Value): The date or datetime in a Value

        Returns:
            Builder: self for chainingd
        """  # TODO: allow date datetime or Value  # pylint: disable=fixme
        self.snapshot = date
        return self

    def __str__(self) -> str:
        select = ", ".join(str(s) for s in self.selected)
        where = f" WHERE {self.search}" if self.search else ""
        order = f" ORDER BY {', '.join(self.order)}" if self.order else ""
        asof = f" ASOF {str(self.snapshot)}" if self.snapshot else ""
        return f"SELECT {select} FROM workitems{where}{order}{asof}"
