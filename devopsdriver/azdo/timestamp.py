#!/usr/bin/env python3


""" Tools that help when working with Azure """


from datetime import datetime, timezone


class Timestamp:
    """An Azure timestamp"""

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    US_PER_MS = 1000  # microseconds per millisecond
    US_PER_SEC = 1000 * US_PER_MS  # microseconds per second

    def __init__(self, value: datetime | str | float | int):
        if isinstance(value, datetime):
            self.value = value

        elif isinstance(value, str):
            self.value = Timestamp.__parse_string(value)

        elif isinstance(value, (int, float)):
            self.value = datetime.fromtimestamp(value, tz=timezone.utc)

    def __str__(self) -> str:
        return self.to_string()

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
