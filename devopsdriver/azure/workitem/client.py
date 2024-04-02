#!/usr/bin/env python3

""" Azure WorkItem Client """


class Client:
    """Wraps work item client"""

    def __init__(self, client):
        self.client = client
