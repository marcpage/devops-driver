#!/usr/bin/env python3

"""Testing dataobject"""

from devopsdriver.dataobject import DataObject


def test_dataobject_basic() -> None:
    """tests the basic dataobject"""
    data = DataObject(
        {
            "Test": 5,
            "system.Go": 12,
            "fields": {"harry": 16, "people": [{"name": "john"}, 5, "test"]},
        }
    )
    assert data.test == 5, data.test
    assert data.go == 12, data.go
    assert data.system_go == 12, data.system_go
    assert data.fields.Harry == 16, data.fields.Harry
    assert data.Harry is None, data.Harry
    assert data.fields.people[0].Name == "john", data.fields.people[0].Name
    assert data.fields.people[1] == 5, data.fields.people[1]
    assert data.fields.people[2] == "test", data.fields.people[2]


def test_lookup() -> None:
    """Tests lookup"""
    data = DataObject(
        {
            "url": "https://dev.azure.com/ni/94b22d7b-ad7b-4f5e-88f0-867910f91c94/"
            + "_apis/wit/workItems/956619/revisions/200",
            "fields": {
                "System.WorkItemType": "Initiative",
                "System.State": "Active",
                "System.Reason": "Moved to state Active",
                "System.AssignedTo": {
                    "displayName": "Samant, Abhay",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/"
                    + "_apis/Identities/838da6d7-6336-68fa-9b48-053771a4d16f",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/"
                            + "_apis/GraphProfile/MemberAvatars/"
                            + "aad.M2NkOWZmNWQtMDMwZC03NDNlLTk5OTUtZTc2MGFhZDRhYmM1"
                        }
                    },
                    "id": "838da6d7-6336-68fa-9b48-053771a4d16f",
                    "uniqueName": "abhay.samant@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/"
                    + "_apis/GraphProfile/MemberAvatars/"
                    + "aad.M2NkOWZmNWQtMDMwZC03NDNlLTk5OTUtZTc2MGFhZDRhYmM1",
                    "descriptor": "aad.M2NkOWZmNWQtMDMwZC03NDNlLTk5OTUtZTc2MGFhZDRhYmM1",
                },
                "System.CreatedDate": "2020-01-08T22:59:16.223Z",
                "System.CreatedBy": {
                    "displayName": "Tillerson, Michael",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/"
                    + "_apis/Identities/dc42cd0e-ab09-4553-8516-9efe930b92a2",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/"
                            + "_apis/GraphProfile/MemberAvatars/"
                            + "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2"
                        }
                    },
                    "id": "dc42cd0e-ab09-4553-8516-9efe930b92a2",
                    "uniqueName": "michael.tillerson@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/"
                    + "_apis/GraphProfile/MemberAvatars/"
                    + "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                    "descriptor": "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                },
                "System.ChangedDate": "2021-02-25T16:50:38.367Z",
                "System.ChangedBy": {
                    "displayName": "SVC, tmrdazdoservice1",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/"
                    + "_apis/Identities/760b4082-c90f-6f25-986a-2e22b876ccd7",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/"
                            + "_apis/GraphProfile/MemberAvatars/"
                            + "aad.ODg2NDQ0NGMtNWJlNy03ZWRkLTljOTEtZmJiNTE4MzFlZjFj"
                        }
                    },
                    "id": "760b4082-c90f-6f25-986a-2e22b876ccd7",
                    "uniqueName": "tm-rd-azdo-service-1@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/"
                    + "_apis/GraphProfile/MemberAvatars/"
                    + "aad.ODg2NDQ0NGMtNWJlNy03ZWRkLTljOTEtZmJiNTE4MzFlZjFj",
                    "descriptor": "aad.ODg2NDQ0NGMtNWJlNy03ZWRkLTljOTEtZmJiNTE4MzFlZjFj",
                },
                "System.CommentCount": 0,
                "System.TeamProject": "DevCentral",
                "System.AreaPath": "DevCentral\\Business Units\\ADG\\ElectroMag\\MMIC",
                "System.IterationPath": "DevCentral",
                "Microsoft.VSTS.Common.ActivatedDate": "2021-01-13T17:33:29.453Z",
                "Microsoft.VSTS.Common.ActivatedBy": {
                    "displayName": "Samant, Abhay",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/"
                    + "_apis/Identities/838da6d7-6336-68fa-9b48-053771a4d16f",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/"
                            + "_apis/GraphProfile/MemberAvatars/"
                            + "aad.M2NkOWZmNWQtMDMwZC03NDNlLTk5OTUtZTc2MGFhZDRhYmM1"
                        }
                    },
                    "id": "838da6d7-6336-68fa-9b48-053771a4d16f",
                    "uniqueName": "abhay.samant@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/"
                    + "_apis/GraphProfile/MemberAvatars/"
                    + "aad.M2NkOWZmNWQtMDMwZC03NDNlLTk5OTUtZTc2MGFhZDRhYmM1",
                    "descriptor": "aad.M2NkOWZmNWQtMDMwZC03NDNlLTk5OTUtZTc2MGFhZDRhYmM1",
                },
                "Microsoft.VSTS.Scheduling.TargetDate": "2021-09-30T05:00:00Z",
                "Microsoft.VSTS.Scheduling.StartDate": "2021-01-13T17:21:25.887Z",
                "Microsoft.VSTS.Common.StackRank": 36894149.0,
                "WEF_C397CD3F9AD34F4CB8D9481E56BBB71C_Kanban.Column.Done": False,
                "WEF_5ADB076CBE2147FC82A22EC1842CD4E9_Kanban.Column.Done": False,
                "Custom.ExpectedStartDate": "2021-01-13T17:21:25.887Z",
                "Custom.ExpectedEndDate": "2021-09-30T05:00:00Z",
                "Custom.AssignedToDate": "2021-01-13T17:33:29Z",
                "Custom.DaysUntilAssigned": 370.8,
                "Custom.AllocationLevel": "Level 1",
                "Custom.OfferingAffinity": "Cognitive RF Sensor Prototyping Testbed ",
                "Custom.AeroDefGovAllocation": 100,
                "WEF_E2F7AF0C84D84051A09966884CE567A9_Kanban.Column.Done": False,
                "Custom.InitiativeType": "P&T Managed",
                "Custom.IncludeonPoR": False,
                "Custom.ScopeorQualityRisk": False,
                "Custom.ScheduleRisk": False,
                "Custom.DaysUntilActive": 370.8,
                "System.Description": '<div><img src="https://dev.azure.com/ni/'
                + '94b22d7b-ad7b-4f5e-88f0-867910f91c94/"+"_apis/wit/attachments/'
                + '64027421-bbca-408e-a742-209aa15366a3?fileName=image.png" alt=Image><br></div>',
                "Microsoft.VSTS.Common.AcceptanceCriteria": "<span>Measurement IP library"
                + "<br></span>"
                + "<div>Interactive Examples<br></div><div>For interactive use-case and demos"
                + "<br></div>"
                + "<div>Programming Examples<br></div><div>Demonstrate how to use the MMIC VIs"
                + "<br></div>"
                + "<div>Datasheet with Performance Metrics<br></div>"
                + "<span>Documentation of the system and recommendation about the "
                + "third-party components "
                + "(couplers, switches, cables, adapters and cal-kit)</span>",
                "Custom.DeprecatedFields": "The Iterative planning team is currently "
                + "refactoring Initiatives and Epics.  Expect changes to these two work items "
                + "over the next few months.The below &quot;Legacy Fields&quot; are under "
                + "consideration for removal.  If these fields are needed, contact Green Rives.",
                "WEF_5ADB076CBE2147FC82A22EC1842CD4E9_Kanban.Column": "Active",
                "WEF_C397CD3F9AD34F4CB8D9481E56BBB71C_Kanban.Column": "Active",
                "WEF_E2F7AF0C84D84051A09966884CE567A9_Kanban.Column": "Active",
                "Microsoft.VSTS.Common.StateChangeDate": "2021-01-13T17:33:29Z",
                "System.BoardColumn": "Active",
                "System.BoardColumnDone": False,
                "Custom.ParentID": 1081371,
                "Custom.ParentTitle": "MMIC: SDP Dev Planning",
                "System.Title": "MMIC Reference Architecture for PA/TRM Test Using 5841/5831",
                "Microsoft.VSTS.Scheduling.StoryPoints": 390.6,
                "Custom.CompletedStoryPoints": 180.0,
                "System.Tags": "ADG Offering",
                "System.Parent": 1081371,
            },
            "id": 956619,
            "relations": [
                {
                    "attributes": {"isLocked": False, "name": "Child"},
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/ni/94b22d7b-ad7b-4f5e-88f0-867910f91c94/"
                    + "_apis/wit/workItems/1094328",
                },
                {
                    "attributes": {"isLocked": False, "name": "Child"},
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/ni/94b22d7b-ad7b-4f5e-88f0-867910f91c94/"
                    + "_apis/wit/workItems/956628",
                },
                {
                    "attributes": {"isLocked": False, "name": "Child"},
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/ni/94b22d7b-ad7b-4f5e-88f0-867910f91c94/"
                    + "_apis/wit/workItems/1198202",
                },
                {
                    "attributes": {"isLocked": False, "name": "Parent"},
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": "https://dev.azure.com/ni/94b22d7b-ad7b-4f5e-88f0-867910f91c94/"
                    + "_apis/wit/workItems/1081371",
                },
            ],
            "rev": 200,
        }
    )

    assert data.lookup("/id") == 956619, data.lookup("/id")
    assert (
        data.lookup("/fields/System.Title")
        == "MMIC Reference Architecture for PA/TRM Test Using 5841/5831"
    ), data.lookup("/fields/System.Title")
    assert (
        data.lookup("/relations/(/attributes/name=Parent).first/url.split(/).last.int")
        == 1081371
    ), [data.lookup("/relations/(/attributes/name=Parent).first/url.split(/).last.int")]
    assert data.lookup("/relations/(/attributes/name=Child)/url.split(/).last.int") == [
        1094328,
        956628,
        1198202,
    ], [data.lookup("/relations/(/attributes/name=Child)/url.split(/).last.int")]
    assert data.lookup("/fields/System.State") == "Active", data.lookup(
        "/fields/System.State"
    )
    assert data.lookup("/fields/System.WorkItemType") == "Initiative", data.lookup(
        "/fields/System.WorkItemType"
    )
    assert (
        data.lookup("/fields/System.AreaPath")
        == "DevCentral\\Business Units\\ADG\\ElectroMag\\MMIC"
    ), data.lookup("/fields/System.AreaPath")
    assert data.lookup("/fields/System.IterationPath") == "DevCentral", data.lookup(
        "/fields/System.IterationPath"
    )
    assert data.lookup("/fields/System.Tags") == "ADG Offering", data.lookup(
        "/fields/System.Tags"
    )
    assert int(
        10 * data.lookup("/fields/Microsoft.VSTS.Scheduling.StoryPoints")
    ) == int(10 * 390.6), data.lookup("/fields/Microsoft.VSTS.Scheduling.StoryPoints")

    assert data.lookup("/relations/(/attributes/name=Child)/url.split(/).first") == [
        "https:",
        "https:",
        "https:",
    ], [data.lookup("/relations/(/attributes/name=Child)/url.split(/).first")]

    try:
        data.lookup("/fields/not there")
    except KeyError:
        pass

    try:
        data.lookup("/fields/System.Title/not there")
    except ValueError:
        pass


def test_lookup_missing() -> None:
    """Tests lookup when a key is missing"""
    data = DataObject(
        {
            "url": "https://dev.azure.com/ni/94b22d7b-ad7b-4f5e-88f0-867910f91c94/_apis/"
            + "wit/workItems/949367/revisions/54",
            "fields": {
                "System.AreaPath": "DevCentral\\Business Units\\ADG\\SharedRepo\\MMSsc",
                "System.TeamProject": "DevCentral",
                "System.IterationPath": "DevCentral\\zzzArchive\\Cycles\\Cycle 17\\i77 "
                + "(ends 2020-02-28)",
                "System.WorkItemType": "Research",
                "System.State": "Closed",
                "System.Reason": "Moved to state Closed",
                "System.AssignedTo": {
                    "displayName": "Brown, Andy",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/_apis/Identities/"
                    + "d91becd5-72ba-6967-a84a-6a6708550e20",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                            + "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl"
                        }
                    },
                    "id": "d91becd5-72ba-6967-a84a-6a6708550e20",
                    "uniqueName": "andy.c.brown@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                    + "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl",
                    "descriptor": "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl",
                },
                "System.CreatedDate": "2019-12-10T20:33:08.743Z",
                "System.CreatedBy": {
                    "displayName": "Tillerson, Michael",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/_apis/Identities/"
                    + "dc42cd0e-ab09-4553-8516-9efe930b92a2",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                            + "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2"
                        }
                    },
                    "id": "dc42cd0e-ab09-4553-8516-9efe930b92a2",
                    "uniqueName": "michael.tillerson@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                    + "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                    "descriptor": "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                },
                "System.ChangedDate": "2026-05-07T16:20:55.96Z",
                "System.ChangedBy": {
                    "displayName": "Tillerson, Michael",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/_apis/Identities/"
                    + "dc42cd0e-ab09-4553-8516-9efe930b92a2",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/_apis/GraphProfile/"
                            + "MemberAvatars/aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2"
                        }
                    },
                    "id": "dc42cd0e-ab09-4553-8516-9efe930b92a2",
                    "uniqueName": "michael.tillerson@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                    + "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                    "descriptor": "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                },
                "System.CommentCount": 7,
                "System.Title": "PA: RFSA: Test Bench Architecture (time boxed)",
                "System.BoardColumn": "Closed",
                "System.BoardColumnDone": False,
                "Microsoft.VSTS.Common.StateChangeDate": "2019-12-10T20:33:08.743Z",
                "Microsoft.VSTS.Common.ClosedDate": "2020-02-14T18:17:33.233Z",
                "Microsoft.VSTS.Common.ValueArea": "Business",
                "Microsoft.VSTS.Common.ClosedBy": {
                    "displayName": "Brown, Andy",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/_apis/Identities/"
                    + "d91becd5-72ba-6967-a84a-6a6708550e20",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                            + "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl"
                        }
                    },
                    "id": "d91becd5-72ba-6967-a84a-6a6708550e20",
                    "uniqueName": "andy.c.brown@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                    + "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl",
                    "descriptor": "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl",
                },
                "Microsoft.VSTS.Common.ResolvedDate": "2020-02-06T03:21:28.327Z",
                "Microsoft.VSTS.Common.ResolvedBy": {
                    "displayName": "Brown, Andy",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/_apis/Identities/"
                    + "d91becd5-72ba-6967-a84a-6a6708550e20",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                            + "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl"
                        }
                    },
                    "id": "d91becd5-72ba-6967-a84a-6a6708550e20",
                    "uniqueName": "andy.c.brown@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                    + "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl",
                    "descriptor": "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl",
                },
                "Microsoft.VSTS.Common.StackRank": 388652161.0,
                "Microsoft.VSTS.Scheduling.StoryPoints": 5.0,
                "Custom.PendingValidationBy": {
                    "displayName": "Brown, Andy",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-6afd-42ea-b8cb-e21a431ec8dd/_apis/Identities/"
                    + "d91becd5-72ba-6967-a84a-6a6708550e20",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                            + "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl"
                        }
                    },
                    "id": "d91becd5-72ba-6967-a84a-6a6708550e20",
                    "uniqueName": "andy.c.brown@emerson.com",
                    "imageUrl": "https://dev.azure.com/ni/_apis/GraphProfile/MemberAvatars/"
                    + "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl",
                    "descriptor": "aad.ZDIxNmMzY2EtMDdiMi03MmQ1LWFjMWQtNmJhMThhZDlhN2Zl",
                },
                "Custom.PendingValidationDate": "2020-02-06T03:21:28.327Z",
                "WEF_D8499809B15042DAABC202ECF51A67D8_Kanban.Column": "Closed",
                "WEF_D8499809B15042DAABC202ECF51A67D8_Kanban.Column.Done": False,
                "WEF_C7071942F5474A15BD600E74B97D7C7A_Kanban.Column": "Closed",
                "WEF_C7071942F5474A15BD600E74B97D7C7A_Kanban.Column.Done": False,
                "WEF_42B49516479B4AEEA0D80D89E8893C45_Kanban.Column": "Closed",
                "WEF_42B49516479B4AEEA0D80D89E8893C45_Kanban.Column.Done": False,
                "WEF_3E05701FE5EA4460876365252800813A_Kanban.Column": "Closed",
                "WEF_3E05701FE5EA4460876365252800813A_Kanban.Column.Done": False,
                "System.Description": "<div>As a developer, I need a testbench to measure and "
                + "validate these features and assess performance</div>",
                "Microsoft.VSTS.Common.AcceptanceCriteria": "<ul><li>Expect documentation "
                + 'similar to <a href="https://dev.azure.com/ni/DevCentral/_wiki/wikis/'
                + 'AppCentral.wiki/8216/EV-Battery-Test-System">this EV Battery Test System '
                + "documentation</a></li><li>Purchase HW&nbsp;</li><ul><li>controller, chassis, "
                + "modules, cables, host computer</li><li><br></li></ul><li>Able to deploy SW to "
                + "DUT</li><li>Able to execute tests on DUT</li>"
                + "<li>Able to record test results</li>"
                + "<li><br></li><li>Eventually use DevOps Services</li>"
                + "<ul><li>Deployment Framework</li>"
                + "<li>Test Execution Framework</li>"
                + "<li><span>Test Reporting Framework</span></li></ul></ul>",
            },
            "id": 949367,
            "rev": 54,
        }
    )

    assert (
        data.lookup("/relations/(/attributes/name=Parent).first/url.split(/).last.int")
        is None
    ), [data.lookup("/relations/(/attributes/name=Parent).first/url.split(/).last.int")]
    assert (
        data.lookup("/relations/(/attributes/name=Child)/url.split(/).last.int", [])
        == []
    ), [data.lookup("/relations/(/attributes/name=Child)/url.split(/).last.int", [])]


if __name__ == "__main__":
    test_lookup_missing()
    test_lookup()
    test_dataobject_basic()
