#!/usr/bin/env python3

"""Manages GitHub connection"""


from github import Github as Github_connection, Auth

from devopsdriver.settings import Settings


class Github:
    """Manages the GitHub connection"""

    def __init__(self, settings: Settings):
        self.settings: Settings = settings
        self.connection: Github_connection | None = None
        assert settings.get("github.token") is not None, "github.token not set"

    def __enter__(self) -> Github_connection:
        self.connection = Github_connection(
            auth=Auth.Token(self.settings["github.token"])
        )
        return self.connection

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self.connection is not None:
            self.connection.close()
