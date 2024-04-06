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


class Field:  # pylint: disable=too-few-public-methods
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
        "CreatedDate",
    }
    COMMON = {"Priority"}

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        if self.value in Field.SYSTEM:
            prefix = "System."

        elif self.value in Field.COMMON:
            prefix = "Microsoft.VSTS.Common."

        else:
            prefix = ""

        return f"[{prefix}{self.value}]"


class OrderBy:  # pylint: disable=too-few-public-methods
    """Order by field"""

    def __init__(self, field: Field | str, order: str = "DESC"):
        self.field = field if isinstance(field, Field) else Field(field)
        self.order = order

    def __str__(self) -> str:
        return f"{self.field} {self.order}"


class Ascending(OrderBy):  # pylint: disable=too-few-public-methods
    """Order by field ascending"""

    def __init__(self, field: Field | str):
        super().__init__(field, "ASC")


class Descending(OrderBy):  # pylint: disable=too-few-public-methods
    """Order by field descending"""

    def __init__(self, field: Field | str):
        super().__init__(field, "DESC")


class Value:  # pylint: disable=too-few-public-methods
    """A constant value"""

    def __init__(self, value: date | datetime | int | float | str):
        self.value = value

    def __str__(self) -> str:
        if isinstance(self.value, datetime):
            return f'"{self.value.strftime("%m/%d/%Y %H:%M:%S")}"'

        if isinstance(self.value, date):
            return f'"{self.value.strftime("%m/%d/%Y")}"'

        if isinstance(self.value, int):
            return str(self.value)

        if isinstance(self.value, float):
            return f"{self.value:0.3f}"

        if isinstance(self.value, str):
            return f'"{self.value}"'  # TODO: escape value  # pylint: disable=fixme

        raise AssertionError("Unknown type")


class IsEmpty:  # pylint: disable=too-few-public-methods
    """Compare a field to a value"""

    def __init__(self, field: Field | str):
        self.field = field if isinstance(field, Field) else Field(field)

    def __str__(self) -> str:
        return f"{str(self.field)} IS EMPTY"


class IsNotEmpty:  # pylint: disable=too-few-public-methods
    """Compare a field to a value"""

    def __init__(self, field: Field | str):
        self.field = field if isinstance(field, Field) else Field(field)

    def __str__(self) -> str:
        return f"{str(self.field)} IS NOT EMPTY"


class Compare:  # pylint: disable=too-few-public-methods
    """Compare a field to a value"""

    def __init__(
        self,
        field: Field | str,
        value: Value | str | date | datetime | int | float,
        operator: str,
    ):
        self.left = field if isinstance(field, Field) else Field(field)
        self.right = value if isinstance(value, Value) else Value(value)
        self.operator = operator

    def __str__(self) -> str:
        return f"{str(self.left)} {self.operator} {str(self.right)}"


class Equal(Compare):  # pylint: disable=too-few-public-methods
    """checks for equality"""

    def __init__(
        self, field: Field | str, value: Value | str | date | datetime | int | float
    ):
        super().__init__(field, value, "=")


class NotEqual(Compare):  # pylint: disable=too-few-public-methods
    """checks for equality"""

    def __init__(
        self, field: Field | str, value: Value | str | date | datetime | int | float
    ):
        super().__init__(field, value, "<>")


class LessThan(Compare):  # pylint: disable=too-few-public-methods
    """checks for lass than"""

    def __init__(
        self, field: Field | str, value: Value | str | date | datetime | int | float
    ):
        super().__init__(field, value, "<")


class GreaterThan(Compare):  # pylint: disable=too-few-public-methods
    """checks for greater than"""

    def __init__(
        self, field: Field | str, value: Value | str | date | datetime | int | float
    ):
        super().__init__(field, value, ">")


class LessThanOrEqual(Compare):  # pylint: disable=too-few-public-methods
    """checks for less than or equal"""

    def __init__(
        self, field: Field | str, value: Value | str | date | datetime | int | float
    ):
        super().__init__(field, value, "<=")


class GreaterThanOrEqual(Compare):  # pylint: disable=too-few-public-methods
    """checks for greater than or equal"""

    def __init__(
        self, field: Field | str, value: Value | str | date | datetime | int | float
    ):
        super().__init__(field, value, ">=")


class Expression:  # pylint: disable=too-few-public-methods
    """Join several compares"""

    def __init__(self, operator: str, *compares: list[Compare]):
        self.operator = operator
        self.expressions = compares

    def __str__(self) -> str:
        return f" {self.operator} ".join(str(e) for e in self.expressions)


class And(Expression):  # pylint: disable=too-few-public-methods
    """Join compares via AND"""

    def __init__(self, *compares: list[Compare | Expression]):
        super().__init__("AND", *compares)


class Or(Expression):  # pylint: disable=too-few-public-methods
    """join compares via OR"""

    def __init__(self, *compares: list[Compare | Expression]):
        super().__init__("OR", *compares)


class Wiql:
    """Build a WIQL query"""

    def __init__(self):
        self.selected = [Field("Id")]
        self.search = None
        self.order = []
        self.snapshot = None

    def select(self, *fields: list[Field | str]):
        """The fields to select

        Returns:
            Builder: Returns self for chaining
        """
        self.selected = [f if isinstance(f, Field) else Field(f) for f in fields]
        return self

    def where(self, expression: Compare | And | Or):
        """Search criteria

        Args:
            expression (Expression|Compare): An expression of what to search for.

        Returns:
            Builder: self for chaining calls
        """
        self.search = expression
        return self

    def order_by(self, *orders):
        """Set the fields to order the results by

        Returns:
            Builder: Returns self for chaining
        """
        self.order = orders
        return self

    def asof(self, stamp: Value | date | datetime | str):
        """Set the view of the data

        Args:
            stamp (Value): The date or datetime in a Value

        Returns:
            Builder: self for chainingd
        """
        assert isinstance(stamp, (Value, date, datetime, str)), stamp
        self.snapshot = stamp if isinstance(stamp, (Value, str)) else Value(stamp)
        return self

    def __str__(self) -> str:
        select = ", ".join(str(s) for s in self.selected)
        where = f" WHERE {self.search}" if self.search else ""
        order = (
            f" ORDER BY {', '.join(str(o) for o in self.order)}" if self.order else ""
        )
        asof = f" ASOF {str(self.snapshot)}" if self.snapshot else ""
        return f"SELECT {select} FROM workitems{where}{order}{asof}"
