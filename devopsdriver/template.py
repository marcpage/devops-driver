#!/usr/bin/env python3


"""Module Doc"""

from os.path import dirname, basename, splitext

from mako.lookup import TemplateLookup
from jinja2 import Environment, FileSystemLoader


class Template:  # pylint: disable=too-few-public-methods
    """Render template files using Mako or Jinja2."""

    def __init__(self, file: str, *search_dirs, extension=None):
        self.template = file
        self.extension = extension
        directories = [dirname(file), *search_dirs]
        self.lookup = TemplateLookup(
            directories=directories,
            output_encoding="utf-8",
            module_directory="/tmp/mako_modules",
        )

        self.jinja = Environment(
            loader=FileSystemLoader(directories),
        )

    def render(self, **args) -> str:
        """Given a set of arguments, render the template.

        Args:
            args (dict): variables and their values

        Returns:
            str: The rendered template
        """
        name = basename(self.template)
        base, extension = splitext(name)

        if self.extension:
            name = base + self.extension
            extension = self.extension

        elif extension == ".py":
            name = base + ".html.mako"
            extension = ".mako"

        if extension == ".j2":
            return self.jinja.get_template(name).render(**args)

        value = self.lookup.get_template(name).render(**args)
        assert isinstance(value, bytes), value.__class__
        return value.decode("utf-8")
