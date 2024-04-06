#!/usr/bin/env python3


""" Module Doc """


from os.path import dirname, basename, splitext

from mako.lookup import TemplateLookup


class Template:  # pylint: disable=too-few-public-methods
    """render template files"""

    def __init__(self, file: str, *search_dirs, extension=None):
        self.template = file
        self.extension = extension
        self.lookup = TemplateLookup(
            directories=[dirname(file), *search_dirs],
            output_encoding="utf-8",
            module_directory="/tmp/mako_modules",
        )

    def render(self, **args) -> str:
        """Given a set of arguments, render the template

        Args:
            args (dict): variables and their values

        Returns:
            str: The rendered template
        """
        name = basename(self.template)
        base, extension = splitext(name)

        if self.extension:
            name = base + self.extension

        elif extension == ".py":
            name = base + ".html.mako"

        return self.lookup.get_template(name).render(**args).decode("utf-8")
