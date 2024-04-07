#!/usr/bin/env python3


""" Tools that help when working with Azure """


from datetime import datetime, timezone, timedelta
from functools import total_ordering


@total_ordering
class Timestamp:
    """An Azure timestamp"""

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    US_PER_MS = 1000  # microseconds per millisecond
    US_PER_SEC = 1000 * US_PER_MS  # microseconds per second

    @staticmethod
    def is_timestamp(value: any) -> bool:
        """Determines if the value is a timestamp string

        Args:
            value (any): The value to check

        Returns:
            bool: True if the value is an Azure timestamp
        """
        if not isinstance(value, str):
            return False

        if not value.endswith("Z"):
            return False

        try:
            Timestamp.__parse_string(value)
            return True

        except ValueError:
            return False

    @staticmethod
    def now():
        """Returns a timestamp representing now"""
        return Timestamp(datetime.now(tz=timezone.utc))

    def __init__(self, value: datetime | str | float | int):
        if isinstance(value, datetime):
            self.value = value

        elif isinstance(value, str):
            self.value = Timestamp.__parse_string(value)

        elif isinstance(value, (int, float)):
            self.value = datetime.fromtimestamp(value, tz=timezone.utc)

    def __str__(self) -> str:
        return self.to_string()

    def __lt__(self, other) -> bool:
        match Timestamp.__comparison_type(other):
            case 1:
                return self.value < other.value
            case 2:
                return self.value < other
            case _:
                return NotImplemented

    def __eq__(self, other) -> bool:
        match Timestamp.__comparison_type(other):
            case 1:
                return self.value == other.value
            case 2:
                return self.value == other
            case _:
                return NotImplemented

    def __sub__(self, other):
        match Timestamp.__comparison_type(other):
            case 1:
                return self.value - other.value
            case 2 | 3:
                return self.value - other
            case _:
                return NotImplemented

    def __add__(self, other):
        if Timestamp.__comparison_type(other) != 3:
            return NotImplemented

        return Timestamp(self.value + other)

    def to_string(self) -> str:
        """Returns the Azure formatted timestamp

        Returns:
            str: The correctly formatted string
        """
        milliseconds = f"{self.value.microsecond / Timestamp.US_PER_MS:03.0f}".rstrip(
            "0"
        )
        return f"{self.value.strftime(Timestamp.DATE_FORMAT)}.{milliseconds}Z"

    def to_timestamp(self) -> float:
        """Converts to a number to use with time.time()

        Returns:
            float: The number of seconds since the epoch
        """
        return datetime.timestamp(self.value)

    @staticmethod
    def __parse_string(timestamp: str) -> datetime:
        assert timestamp.endswith("Z"), timestamp
        whole, fractional = timestamp.rsplit(".", 1)
        result = datetime.strptime(whole, Timestamp.DATE_FORMAT)
        fractional_seconds = float(f"0.{fractional[:-1].ljust(3, '0')}")
        return result.replace(
            microsecond=int(fractional_seconds * Timestamp.US_PER_SEC)
        ).replace(tzinfo=timezone.utc)

    @staticmethod
    def __comparison_type(other) -> int:
        if isinstance(other, timedelta):
            return 3

        if isinstance(other, datetime):
            return 2

        if hasattr(other, "value") and isinstance(other.value, datetime):
            return 1

        return 0
