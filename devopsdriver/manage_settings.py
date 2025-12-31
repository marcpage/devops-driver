#!/usr/bin/env python3


"""Module Doc"""


from os.path import dirname, join, abspath
from sys import argv as sys_argv
from getpass import getpass as os_getpass

from keyring import set_password

from .settings import Settings
from .template import Template

ARGV = sys_argv
PRINT = print  # pylint: disable=invalid-name
SET_PASSWORD = set_password  # pylint: disable=invalid-name
GET_PASS = os_getpass  # pylint: disable=invalid-name


def main() -> None:
    """Get settings values"""
    args = list(ARGV[1:])

    if not args or "--help" in args or "-h" in args:
        PRINT(
            Template(
                __file__, join(dirname(__file__), "templates"), extension=".txt.mako"
            ).render()
        )
        return

    position = args.index("--script") if "--script" in args else len(args)
    script = __file__

    if position + 1 < len(args):
        args.pop(position)
        script = abspath(args.pop(position))

    settings = Settings(script, dirname(dirname(__file__))).key("secrets")

    if "--secrets" in args:
        args.remove("--secrets")

        for secret, key in settings.secrets.items():
            PRINT(f"secret: {secret}  key: {key}")

            if not settings.has(secret):
                value = GET_PASS(f"{secret} ({key}): ")

                if value:
                    SET_PASSWORD(*Settings.split_key(key), value)
            else:
                PRINT("\tValue set")

    for arg in args:
        PRINT(f"{settings.get(arg)}")


if __name__ == "__main__":
    main()
