#!/usr/bin/env python3

""" Azure Pipeline Run Log """

from azure.devops.v7_1.pipelines.models import Pipeline
from azure.devops.v7_1.pipelines.models import Run
from azure.devops.v7_1.pipelines.models import Log as AzureLog
from azure.devops.v7_1.pipelines import PipelinesClient

from requests import get


class Log:
    def __init__(
        self,
        client: PipelinesClient,
        project: str,
        pipeline: Pipeline,
        run: Run,
        log: AzureLog,
    ):
        self.client = client
        self.project = project
        self.pipeline = pipeline
        self.run = run
        self.log = log
        self.text = get(self.log.signed_content.url, timeout=1).text


#!/usr/bin/env python3

""" Notify users of Work Items that are In Progress or On Hold a period of time"""

from datetime import date, datetime, timedelta, timezone

from azure.devops.v7_1.pipelines import PipelinesClient
import requests

from devopsdriver.settings import Settings
from devopsdriver.azdo import Azure, Timestamp
from devopsdriver.azdo import Wiql, LessThan, And, In

__version__ = "0.0.1"

FIRST = 0
LAST = -1
MICROSECONDS_PER_SECOND = 1000 * 1000


def scrape_build_logs(azure: Azure):
    pc: PipelinesClient = azure.connection.clients_v7_1.get_pipelines_client()
    pipelines = pc.list_pipelines("Creative")

    for pipeline in pipelines:
        print(f"Pipeline: {pipeline.name}")
        runs = pc.list_runs("Creative", pipeline.id)

        for run in runs:
            print(
                f"\t Run: {run.name} on {run.finished_date.strftime('%Y/%m/%d %H:%M:%S')}"
            )
            logs = pc.list_logs("Creative", pipeline.id, run.id, expand="signedContent")
            for log in logs.logs:
                print(
                    f"{'='*10} {log.last_changed_on.strftime('%Y/%m/%d %H:%M:%S')} {'='*10}"
                )
                print(requests.get(log.signed_content.url, timeout=1).text)
            break
        break


""" pipeline
"folder": "\\",
"id": 1,
"name": "DevOps",
"revision": 1,
"_links": {},
"url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1?revision=1"
"""

""" run
"id": 1,
"name": "20240325.1",
"_links": {},
"created_date": "2024-03-25T23:53:38.503126Z",
"finished_date": "2024-03-25T23:53:43.467565Z",
"pipeline": {
    "folder": "\\",
    "id": 1,
    "name": "DevOps",
    "revision": 1,
    "url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1?revision=1"
},
"result": "failed",
"state": "completed",
"template_parameters": {},
"url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1/runs/1"
"""

""" log with expand=signedContent
"created_on": "2024-04-08T23:00:59.020Z",
"id": 8,
"last_changed_on": "2024-04-08T23:00:59.160Z",
"line_count": 4,
"signed_content": {
    "signature_expires": "2024-04-10T01:06:18.306299Z",
    "url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1/runs/10/signedlogcontent/8?urlExpires=2024-04-10T01%3A06%3A18.3062992Z&urlSigningMethod=HMACV1&urlSignature=2pv0SC3rVbDJwLdzNBUoCTfQc0VgPvndxkw2aB3g9iA%3D"
},
"url": "https://dev.azure.com/OakAI/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/_apis/pipelines/1/runs/10/logs/8"
"""


def main() -> None:
    """BadgerBot"""
    settings = Settings(__file__).key("secrets").cli("cli").env("env")
    azure = Azure(settings)
    scrape_build_logs(azure)
    return
    staleness = settings["stale limit in days"]
    newest_stale = min(d for p, d in staleness.items())
    days_ago = date.today() - timedelta(days=newest_stale)
    stale = azure.workitem.find(
        Wiql().where(
            And(
                LessThan("ChangedDate", days_ago),
                In("State", *settings["active states"]),
            )
        )
    )
    print(__import__("json").dumps(stale[0][0].raw.as_dict(), indent=2))
    people = {
        i[LAST].assignedTo.displayName for i in stale if i[0].assignedTo is not None
    }
    print(
        f"stale people with no opt-in: {', '.join(p for p in people if p not in staleness)}"
    )
    by_person = {
        p: [
            i
            for i in stale
            if i[LAST].assignedTo is not None
            and i[LAST].assignedTo.displayName == p
            and p in staleness
            and (datetime.now(tz=timezone.utc) - i[LAST].ChangedDate.value).days
            >= staleness[p]
        ]
        for p in people
    }

    for person, stale_items in by_person.items():
        if not stale_items:
            continue

        print(person)

        for item in sorted(
            stale_items, key=lambda i: i[LAST].changedDate, reverse=True
        ):
            print(
                f"\t {(Timestamp.now() - item[LAST].ChangedDate).days} "
                + f"days ago: #{item[LAST].id} {item[LAST].title}"
            )


if __name__ == "__main__":
    main()
