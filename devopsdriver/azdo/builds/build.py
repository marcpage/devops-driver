#!/usr/bin/env python3

""" Azure Build """

from azure.devops.v7_1.build.models import Build as AzureBuild
from azure.devops.v7_1.build import BuildClient
from azure.devops.v7_1.build.models import TimelineRecord

from devopsdriver.azdo import AzureObject


class Build(AzureObject):  # pylint: disable=too-few-public-methods
    """Azure Build"""

    def __init__(self, client: BuildClient, build: AzureBuild):
        self.client = client
        self.build = build
        super().__init__(build)

    class Step(AzureObject):  # pylint: disable=too-few-public-methods
        """Azure Build Step (job, task, step)"""

        def __init__(self, entry: TimelineRecord):
            self.children = []
            self.log_contents: str = None
            super().__init__(entry)

        def all_logs(self) -> list[str]:
            """Get a list of all logs in chronological order

            Returns:
                list[str]: List of all the logs
            """
            logs = [] if self.log_contents is None else [self.log_contents]

            for child in self.children:
                logs.extend(child.all_logs())

            return logs

    def __add_steps_and_logs(self, entry: Step, to_process: list[Step]) -> Step:
        project = self.build.project.name
        build_id = self.build.id

        if entry.log:
            entry.log_contents = "\n".join(
                self.client.get_build_log_lines(project, build_id, entry.log.id)
            )

        entry.children = [e for e in to_process if e.parent_id == entry.id]

        for child in entry.children:
            to_process.remove(child)
            self.__add_steps_and_logs(child, to_process)

        return entry

    def get_logs(self) -> Step:
        """Gets the logs in a hierarchical structure

        Returns:
            Step: The root element of the log hierarchy
        """
        project = self.build.project.name
        build_id = self.build.id
        steps = [
            Build.Step(r)
            for r in self.client.get_build_timeline(project, build_id).records
        ]
        root = [s for s in steps if not s.parent_id]
        assert len(root) == 1, root
        root = root[0]
        steps.remove(root)
        return self.__add_steps_and_logs(root, steps)
