#!/usr/bin/env python3

""" Testing dataobject """


from devopsdriver.dataobject import DataObject


def test_dataobject_basic() -> None:
    """tests the basic dataobject"""
    data = DataObject(
        {
            "Test": 5,
            "system.Go": 12,
            "fields": {"harry": 16, "people": [{"name": "john"}, 5, "test"]},
        }
    )
    assert data.test == 5, data.test
    assert data.go == 12, data.go
    assert data.system_go == 12, data.system_go
    assert data.fields.Harry == 16, data.fields.Harry
    assert data.Harry is None, data.Harry
    assert data.fields.people[0].Name == "john", data.fields.people[0].Name
    assert data.fields.people[1] == 5, data.fields.people[1]
    assert data.fields.people[2] == "test", data.fields.people[2]


if __name__ == "__main__":
    test_dataobject_basic()
