#!/usr/bin/env python3

""" Test the manage_settings tool """

from os.path import join
from tempfile import TemporaryDirectory
from helpers import setup_settings, write

from devopsdriver import settings
from devopsdriver import manage_settings


def test_main():
    """test the main entry point"""
    with TemporaryDirectory() as working_dir:
        setup_settings(shared="test", Linux=join(working_dir, "Linux"))
        settings.ARGV = ["ignore", "test"]
        manage_settings.ARGV = ["ignore", "test"]
        storage = {}

        def mock_print(message: str) -> None:
            storage["print"] = message

        settings.PRINT = mock_print
        manage_settings.PRINT = mock_print
        write(join(working_dir, "Linux", "test.yml"), test=3)
        manage_settings.main()
        assert storage["print"] == "3", storage


def test_main_help():
    """test the main entry point"""
    with TemporaryDirectory() as working_dir:
        setup_settings(shared="test", Linux=join(working_dir, "Linux"))
        manage_settings.PRINT = settings.PRINT
        settings.ARGV = ["ignore", "--help"]
        manage_settings.ARGV = settings.ARGV
        storage = {}

        def mock_print(message: str) -> None:
            storage["print"] = message

        settings.PRINT = mock_print
        manage_settings.PRINT = mock_print
        write(join(working_dir, "Linux", "test.yml"), test=3)
        manage_settings.main()
        assert storage["print"].startswith("Usage:"), storage


def test_main_set_secret():
    """test the main entry point when settings keychain secrets"""

    def set_password(s, n, p):
        assert (
            s in ("azure", "jira") and n == "token" and p == "setec astronomy"
        ), f"{s} {n} {p}"

    with TemporaryDirectory() as working_dir:
        setup_settings(shared="test", Linux=join(working_dir, "Linux"))
        settings.ARGV = ["ignore", "--secrets"]
        manage_settings.ARGV = settings.ARGV
        settings.GET_PASSWORD = lambda s, n: (
            "password" if f"{s}/{n}" == "azure/token" else None
        )
        settings.GET_PASS = lambda p: "setec astronomy"
        manage_settings.GET_PASS = settings.GET_PASS
        manage_settings.PRINT = settings.PRINT
        settings.SET_PASSWORD = set_password
        manage_settings.SET_PASSWORD = settings.SET_PASSWORD
        write(
            join(working_dir, "Linux", "test.yml"),
            secrets={"azure.token": "azure/token", "jira.token": "jira/token"},
        )
        manage_settings.main()


if __name__ == "__main__":
    test_main()
    test_main_help()
    test_main_set_secret()
