#!/usr/bin/env python3

""" test Template """

from os.path import join
from tempfile import TemporaryDirectory

from devopsdriver.template import Template


def test_basic() -> None:
    """test the basic usage of the template"""
    with TemporaryDirectory() as working_dir:
        template_path = join(working_dir, "template.html.mako")
        script_path = join(working_dir, "template.py")

        with open(template_path, "w", encoding="utf-8") as template:
            template.write("value = ${value}")

        result = Template(template_path).render(value=5)
        assert result == "value = 5", result
        result = Template(script_path).render(value=5)
        assert result == "value = 5", result
        result = Template(script_path, extension=".html.mako").render(value=5)
        assert result == "value = 5", result


if __name__ == "__main__":
    test_basic()
