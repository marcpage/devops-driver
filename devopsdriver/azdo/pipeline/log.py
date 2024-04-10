#!/usr/bin/env python3

""" Azure Pipeline Run Log """

from azure.devops.v7_1.pipelines.models import Log as AzureLog

from requests import get as get_url

from devopsdriver.azdo.azureobject import AzureObject

GET_URL = get_url


class Log(AzureObject):  # pylint: disable=too-few-public-methods
    """Log fields:
    created_on ("2024-04-08T23:00:59.020Z")
    id (8)
    last_changed_on ("2024-04-08T23:00:59.160Z")
    line_count (4)
    url ("https://dev.azure.com/Org/<guid>/_apis/pipelines/1/runs/10/logs/8")
    """

    def __init__(self, log: AzureLog):
        self.text = GET_URL(log.signed_content.url, timeout=1).text
        super().__init__(log)
