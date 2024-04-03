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


class Field:
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


class OrderBy:
    """Order by field"""

    def __init__(self, field: Field, order: str = "DESC"):
        self.field = field
        self.order = order

    def __str__(self) -> str:
        return f"{self.field} {self.order}"


class Ascending:
    """Order by field ascending"""

    def __init__(self, field: Field):
        self.field = field
        super().__init__(field, "ASC")


class Descending:
    """Order by field descending"""

    def __init__(self, field: Field):
        self.field = field
        super().__init__(field, "DESC")


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

    @staticmethod
    def __format(entity) -> str:
        assert isinstance(entity, datetime) or isinstance(entity, date)
        fmt = "%Y-%m-%d" if isinstance(entity, date) else "%Y-%m-%d %H:%M:%S"
        return f"'{entity.strftime(fmt)}'"

    def __str__(self) -> str:
        select = ", ".join(str(s) for s in self.selected)
        where = f" WHERE {self.search}" if self.search else ""
        order = f" ORDER BY {', '.join(self.order)}" if self.order else ""
        asof = f" ASOF {Builder.__format(self.snapshot)}" if self.snapshot else ""
        return f"SELECT {select} FROM workitems{where}{order}{asof}"
