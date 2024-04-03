#!/usr/bin/env python3

""" Module Doc """

from os import makedirs
from os.path import dirname, splitext
from json import dump

from yaml import safe_dump

from devopsdriver import settings


def setup_settings(os: str = "Linux", shared: str = "test", **pref_dirs) -> None:
    """Setup a mock environment for settings

    Args:
        os (str, optional): The platform to fake. Defaults to "Linux".
        shared (str, optional): The default yaml file name. Defaults to "test".
        pref_dirs (dict, optional): Mapping of platform name to preferences directory
    """
    settings.ENVIRON = {}
    settings.ARGV = []
    settings.SYSTEM = lambda: os
    settings.SHARED = shared
    settings.PRINT = lambda s: s
    settings.GET_PASSWORD = lambda s, n: f"{s}:{n}"
    settings.GET_PASS = lambda p: p
    settings.SET_PASSWORD = lambda s, n, p: f"{s} {n} {p}"
    # settings.MAKEDIRS = lambda p: p
    # settings.Settings.FORMATS = None
    settings.Settings.PREF_DIR = pref_dirs


def ensure(directory: str) -> str:
    """Ensures that a directory exists before using

    Args:
        directory (str): The directory to create

    Returns:
        str: The directory that now exists
    """
    makedirs(directory, exist_ok=True)
    return directory


def write(path: str, **options) -> None:
    """Write a json or yaml file (depends on path extension) of dictionary with given values

    Args:
        path (str): Path to the file to write.
                    If it is .json it will be written in JSON otherwise YAML
        options (dict): the dictionary values to write
    """
    ensure(dirname(path))

    with open(path, "w", encoding="utf-8") as settings_file:
        if splitext(path)[1] == ".json":
            dump(options, settings_file)
        else:
            safe_dump(options, settings_file)
