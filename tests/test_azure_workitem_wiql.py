#!/usr/bin/env python3

""" Test work item query language """

from datetime import date, datetime

from devopsdriver.azdo import Wiql
from devopsdriver.azdo import Ascending, Descending, Value
from devopsdriver.azdo import IsEmpty, IsNotEmpty, And, Or
from devopsdriver.azdo import GreaterThan, LessThan, Equal, NotEqual
from devopsdriver.azdo import GreaterThanOrEqual, LessThanOrEqual


def test_no_params() -> None:
    """Test empty, default wiql"""
    assert str(Wiql()) == "SELECT [System.Id] FROM workitems", str(Wiql())


def test_expressions() -> None:
    """Test much of the expression"""
    start = date(2024, 6, 30)
    end = datetime(2025, 1, 1, 18, 30, 15)
    builder = (
        Wiql()
        .select("State", "Id")
        .where(
            And(
                Equal("State", "New"),
                IsEmpty("Title"),
                IsNotEmpty("Priority"),
                GreaterThan("CreatedDate", start),
                LessThan("CreatedDate", end),
                Or(
                    IsEmpty("RootCause"),
                    NotEqual("Priority", 1),
                    LessThan("Rank", 5.0),
                    LessThanOrEqual("time", 4.0),
                    GreaterThanOrEqual("BusinessValue", 4),
                ),
            )
        )
        .order_by(Descending("Priority"), Ascending("CreatedDate"))
        .asof(start)
    )
    expected = (
        """SELECT [System.State], [System.Id] FROM workitems """
        + """WHERE [System.State] = "New" AND [System.Title] IS EMPTY """
        + """AND [Microsoft.VSTS.Common.Priority] IS NOT EMPTY """
        + """AND [System.CreatedDate] > "06/30/2024" """
        + """AND [System.CreatedDate] < "01/01/2025 18:30:15" AND [RootCause] IS EMPTY """
        + """OR [Microsoft.VSTS.Common.Priority] <> 1 OR [Rank] < 5.000 """
        + """OR [time] <= 4.000 OR [BusinessValue] >= 4 """
        + """ORDER BY [Microsoft.VSTS.Common.Priority] DESC, [System.CreatedDate] ASC """
        + """ASOF "06/30/2024\""""
    )
    assert str(builder) == expected, str(builder)


def test_invalid_value_type() -> None:
    """tests assertion that field has known types"""
    try:
        assert str(Value(test_no_params)) is None, str(Value(test_no_params))

    except AssertionError:
        pass


if __name__ == "__main__":
    test_invalid_value_type()
    test_expressions()
    test_no_params()
