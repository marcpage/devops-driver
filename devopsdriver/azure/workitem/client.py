#!/usr/bin/env python3

""" Azure WorkItem Client """


class Client:  # pylint: disable=too-few-public-methods
    """Wraps work item client"""

    def __init__(self, client):
        self.client = client
