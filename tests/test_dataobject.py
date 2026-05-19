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
            "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
            + "_apis/wit/workItems/956619/revisions/200",
            "fields": {
                "System.WorkItemType": "Initiative",
                "System.State": "Active",
                "System.Reason": "Moved to state Active",
                "System.AssignedTo": {
                    "displayName": "User One",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/"
                    + "_apis/Identities/838da6d7-68fa-9b48-6336-053771a4d16f",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/"
                            + "_apis/GraphProfile/MemberAvatars/"
                            + "aad.mM1M2NkOWGFhZDRhYZmNWQtMTUtZTc2MDMwZC03NDNlLTk5O"
                        }
                    },
                    "id": "838da6d7-68fa-9b48-6336-053771a4d16f",
                    "uniqueName": "user1@company.com",
                    "imageUrl": "https://dev.azure.com/company/"
                    + "_apis/GraphProfile/MemberAvatars/"
                    + "aad.mM1M2NkOWGFhZDRhYZmNWQtMTUtZTc2MDMwZC03NDNlLTk5O",
                    "descriptor": "aad.mM1M2NkOWGFhZDRhYZmNWQtMTUtZTc2MDMwZC03NDNlLTk5O",
                },
                "System.CreatedDate": "2020-01-08T22:59:16.223Z",
                "System.CreatedBy": {
                    "displayName": "User Two",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/"
                    + "_apis/Identities/dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/"
                            + "_apis/GraphProfile/MemberAvatars/"
                            + "aad.mE2YWZkMzTcwMmM1Mg2MTItMDQtMTY1YTAwMy03YmM1LWI1O"
                        }
                    },
                    "id": "dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "uniqueName": "user2@company.com",
                    "imageUrl": "https://dev.azure.com/company/"
                    + "_apis/GraphProfile/MemberAvatars/"
                    + "aad.mE2YWZkMzTcwMmM1Mg2MTItMDQtMTY1YTAwMy03YmM1LWI1O",
                    "descriptor": "aad.mE2YWZkMzTcwMmM1Mg2MTItMDQtMTY1YTAwMy03YmM1LWI1O",
                },
                "System.ChangedDate": "2021-02-25T16:50:38.367Z",
                "System.ChangedBy": {
                    "displayName": "Service Account",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/"
                    + "_apis/Identities/760b4082-6f25-986a-c90f-2e22b876ccd7",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/"
                            + "_apis/GraphProfile/MemberAvatars/"
                            + "aad.jFjODg2NDTE4MzFlZQ0NGMtNTEtZmJiNWJlNy03ZWRkLTljO"
                        }
                    },
                    "id": "760b4082-6f25-986a-c90f-2e22b876ccd7",
                    "uniqueName": "azdo-service@company.com",
                    "imageUrl": "https://dev.azure.com/company/"
                    + "_apis/GraphProfile/MemberAvatars/"
                    + "aad.jFjODg2NDTE4MzFlZQ0NGMtNTEtZmJiNWJlNy03ZWRkLTljO",
                    "descriptor": "aad.jFjODg2NDTE4MzFlZQ0NGMtNTEtZmJiNWJlNy03ZWRkLTljO",
                },
                "System.CommentCount": 0,
                "System.TeamProject": "Project",
                "System.AreaPath": "Project\\Group\\Area\\Product\\Team3",
                "System.IterationPath": "Project",
                "Microsoft.VSTS.Common.ActivatedDate": "2021-01-13T17:33:29.453Z",
                "Microsoft.VSTS.Common.ActivatedBy": {
                    "displayName": "User One",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/"
                    + "_apis/Identities/838da6d7-68fa-9b48-6336-053771a4d16f",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/"
                            + "_apis/GraphProfile/MemberAvatars/"
                            + "aad.mM1M2NkOWGFhZDRhYZmNWQtMTUtZTc2MDMwZC03NDNlLTk5O"
                        }
                    },
                    "id": "838da6d7-68fa-9b48-6336-053771a4d16f",
                    "uniqueName": "user1@company.com",
                    "imageUrl": "https://dev.azure.com/company/"
                    + "_apis/GraphProfile/MemberAvatars/"
                    + "aad.mM1M2NkOWGFhZDRhYZmNWQtMTUtZTc2MDMwZC03NDNlLTk5O",
                    "descriptor": "aad.mM1M2NkOWGFhZDRhYZmNWQtMTUtZTc2MDMwZC03NDNlLTk5O",
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
                "Custom.OfferingAffinity": "The offering affinity ",
                "Custom.AeroDefGovAllocation": 100,
                "WEF_E2F7AF0C84D84051A09966884CE567A9_Kanban.Column.Done": False,
                "Custom.InitiativeType": "P&T Managed",
                "Custom.IncludeonPoR": False,
                "Custom.ScopeorQualityRisk": False,
                "Custom.ScheduleRisk": False,
                "Custom.DaysUntilActive": 370.8,
                "System.Description": '<div><img src="https://dev.azure.com/company/'
                + '94b22d7b-4f5e-88f0-ad7b-867910f91c94/"+"_apis/wit/attachments/'
                + '64027421-408e-a742-bbca-209aa15366a3?fileName=image.png" alt=Image><br></div>',
                "Microsoft.VSTS.Common.AcceptanceCriteria": "<span>Measurement IP library"
                + "<br></span>"
                + "<div>Interactive Examples<br></div><div>For interactive use-case and demos"
                + "<br></div>"
                + "<div>Programming Examples<br></div><div>Demonstrate how to use the Stuff"
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
                "Custom.ParentTitle": "Project: SDP Dev Planning",
                "System.Title": "Project Reference Architecture for PA/TRM Test Using 541/531",
                "Microsoft.VSTS.Scheduling.StoryPoints": 390.6,
                "Custom.CompletedStoryPoints": 180.0,
                "System.Tags": "Business Offering",
                "System.Parent": 1081371,
            },
            "id": 956619,
            "relations": [
                {
                    "attributes": {"isLocked": False, "name": "Child"},
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
                    + "_apis/wit/workItems/1094328",
                },
                {
                    "attributes": {"isLocked": False, "name": "Child"},
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
                    + "_apis/wit/workItems/956628",
                },
                {
                    "attributes": {"isLocked": False, "name": "Child"},
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
                    + "_apis/wit/workItems/1198202",
                },
                {
                    "attributes": {"isLocked": False, "name": "Parent"},
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
                    + "_apis/wit/workItems/1081371",
                },
            ],
            "rev": 200,
        }
    )

    assert data.lookup("/id") == 956619, data.lookup("/id")
    assert (
        data.lookup("/fields/System.Title")
        == "Project Reference Architecture for PA/TRM Test Using 541/531"
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
        data.lookup("/fields/System.AreaPath") == "Project\\Group\\Area\\Product\\Team3"
    ), data.lookup("/fields/System.AreaPath")
    assert data.lookup("/fields/System.IterationPath") == "Project", data.lookup(
        "/fields/System.IterationPath"
    )
    assert data.lookup("/fields/System.Tags") == "Business Offering", data.lookup(
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
            "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/_apis/"
            + "wit/workItems/949367/revisions/54",
            "fields": {
                "System.AreaPath": "Project\\Group\\Area\\Product\\Team2",
                "System.TeamProject": "Project",
                "System.IterationPath": "Project\\zzzArchive\\Cycles\\Cycle 17\\i77 "
                + "(ends 2020-02-28)",
                "System.WorkItemType": "Research",
                "System.State": "Closed",
                "System.Reason": "Moved to state Closed",
                "System.AssignedTo": {
                    "displayName": "User Three",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/_apis/Identities/"
                    + "d91becd5-6967-a84a-72ba-6a6708550e20",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/_apis/GraphProfile/"
                            + "MemberAvatars/"
                            + "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM"
                        }
                    },
                    "id": "d91becd5-6967-a84a-72ba-6a6708550e20",
                    "uniqueName": "user3@company.com",
                    "imageUrl": "https://dev.azure.com/company/_apis/GraphProfile/MemberAvatars/"
                    + "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM",
                    "descriptor": "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM",
                },
                "System.CreatedDate": "2019-12-10T20:33:08.743Z",
                "System.CreatedBy": {
                    "displayName": "User Two",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/_apis/Identities/"
                    + "dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/_apis/GraphProfile/"
                            + "MemberAvatars/"
                            + "aad.mE2YWZkMzTcwMmM1Mg2MTItMDQtMTY1YTAwMy03YmM1LWI1O"
                        }
                    },
                    "id": "dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "uniqueName": "user2@company.com",
                    "imageUrl": "https://dev.azure.com/company/_apis/GraphProfile/MemberAvatars/"
                    + "aad.mE2YWZkMzTcwMmM1Mg2MTItMDQtMTY1YTAwMy03YmM1LWI1O",
                    "descriptor": "aad.mE2YWZkMzTcwMmM1Mg2MTItMDQtMTY1YTAwMy03YmM1LWI1O",
                },
                "System.ChangedDate": "2026-05-07T16:20:55.96Z",
                "System.ChangedBy": {
                    "displayName": "User Two",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/_apis/Identities/"
                    + "dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/_apis/GraphProfile/"
                            + "MemberAvatars/aad.mE2YWZkMzTcwMmM1Mg2MTItMDQtMTY1YTAwMy03YmM1LWI1O"
                        }
                    },
                    "id": "dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "uniqueName": "user2@company.com",
                    "imageUrl": "https://dev.azure.com/company/_apis/GraphProfile/MemberAvatars/"
                    + "aad.mE2YWZkMzTcwMmM1Mg2MTItMDQtMTY1YTAwMy03YmM1LWI1O",
                    "descriptor": "aad.mE2YWZkMzTcwMmM1Mg2MTItMDQtMTY1YTAwMy03YmM1LWI1O",
                },
                "System.CommentCount": 7,
                "System.Title": "PA: RFSA: Test Bench Architecture (time boxed)",
                "System.BoardColumn": "Closed",
                "System.BoardColumnDone": False,
                "Microsoft.VSTS.Common.StateChangeDate": "2019-12-10T20:33:08.743Z",
                "Microsoft.VSTS.Common.ClosedDate": "2020-02-14T18:17:33.233Z",
                "Microsoft.VSTS.Common.ValueArea": "Business",
                "Microsoft.VSTS.Common.ClosedBy": {
                    "displayName": "User Three",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/_apis/Identities/"
                    + "d91becd5-6967-a84a-72ba-6a6708550e20",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/_apis/GraphProfile/"
                            + "MemberAvatars/"
                            + "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM"
                        }
                    },
                    "id": "d91becd5-6967-a84a-72ba-6a6708550e20",
                    "uniqueName": "user3@company.com",
                    "imageUrl": "https://dev.azure.com/company/_apis/GraphProfile/MemberAvatars/"
                    + "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM",
                    "descriptor": "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM",
                },
                "Microsoft.VSTS.Common.ResolvedDate": "2020-02-06T03:21:28.327Z",
                "Microsoft.VSTS.Common.ResolvedBy": {
                    "displayName": "User Three",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/_apis/Identities/"
                    + "d91becd5-6967-a84a-72ba-6a6708550e20",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/_apis/GraphProfile/"
                            + "MemberAvatars/"
                            + "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM"
                        }
                    },
                    "id": "d91becd5-6967-a84a-72ba-6a6708550e20",
                    "uniqueName": "user3@company.com",
                    "imageUrl": "https://dev.azure.com/company/_apis/GraphProfile/MemberAvatars/"
                    + "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM",
                    "descriptor": "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM",
                },
                "Microsoft.VSTS.Common.StackRank": 388652161.0,
                "Microsoft.VSTS.Scheduling.StoryPoints": 5.0,
                "Custom.PendingValidationBy": {
                    "displayName": "User Three",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/_apis/Identities/"
                    + "d91becd5-6967-a84a-72ba-6a6708550e20",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/_apis/GraphProfile/"
                            + "MemberAvatars/"
                            + "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM"
                        }
                    },
                    "id": "d91becd5-6967-a84a-72ba-6a6708550e20",
                    "uniqueName": "user3@company.com",
                    "imageUrl": "https://dev.azure.com/company/_apis/GraphProfile/MemberAvatars/"
                    + "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM",
                    "descriptor": "aad.2ZlZDIxNmThhZDlhNMzY2EtMWQtNmJhMDdiMi03MmQ1LWFjM",
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
                + 'similar to <a href="https://dev.azure.com/company/Project/_wiki/wikis/'
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


def test_no_parent() -> None:
    """Tests the case where there is no Parent relationship"""
    data = DataObject(
        {
            "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
            + "_apis/wit/workItems/957647/revisions/197",
            "fields": {
                "System.AreaPath": "Project\\Group\\Area\\Product\\Team3",
                "System.TeamProject": "Project",
                "System.IterationPath": "Project",
                "System.WorkItemType": "Initiative",
                "System.State": "Concept",
                "System.Reason": "Moved to state Concept",
                "System.CreatedDate": "2020-01-10T16:43:45.98Z",
                "System.CreatedBy": {
                    "displayName": "Sam Smith",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/_apis/Identities/"
                    + "dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/_apis/GraphProfile/"
                            + "MemberAvatars/aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2"
                        }
                    },
                    "id": "dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "uniqueName": "user6@emerson.com",
                    "imageUrl": "https://dev.azure.com/company/_apis/GraphProfile/"
                    + "MemberAvatars/aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                    "descriptor": "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                },
                "System.ChangedDate": "2026-04-28T20:52:23.37Z",
                "System.ChangedBy": {
                    "displayName": "Harry Styles",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/_apis/Identities/"
                    + "6291af6c-651f-8121-62aa-5df76b8a32b7",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/company/_apis/GraphProfile/"
                            + "MemberAvatars/aad.NjI5MWFmNmMtNjJhYS03NTFmLTgxMjEtNWRmNzZiOGEzMmI3"
                        }
                    },
                    "id": "6291af6c-651f-8121-62aa-5df76b8a32b7",
                    "uniqueName": "user5@emerson.com",
                    "imageUrl": "https://dev.azure.com/company/_apis/GraphProfile/"
                    + "MemberAvatars/aad.NjI5MWFmNmMtNjJhYS03NTFmLTgxMjEtNWRmNzZiOGEzMmI3",
                    "descriptor": "aad.NjI5MWFmNmMtNjJhYS03NTFmLTgxMjEtNWRmNzZiOGEzMmI3",
                },
                "System.CommentCount": 0,
                "System.Title": "Customer Specific Opportunities",
                "System.BoardColumnDone": False,
                "Microsoft.VSTS.Common.StateChangeDate": "2025-07-02T12:40:49Z",
                "Microsoft.VSTS.Common.StackRank": 36888929.0,
                "Microsoft.VSTS.Scheduling.StoryPoints": 137.5,
                "Custom.CompletedStoryPoints": 111.5,
                "WEF_C397CD3F9AD34F4CB8D9481E56BBB71C_Kanban.Column.Done": False,
                "WEF_5ADB076CBE2147FC82A22EC1842CD4E9_Kanban.Column.Done": False,
                "Custom.CustomerCommitment": False,
                "Custom.InitiativeType": "PR&D Internal",
                "Custom.WIRLastSeenUpdate": 203,
                "Custom.IsMilestone": False,
                "Custom.IncludeinPowerBIReports": False,
                "Custom.InitiativeStatus": "Requested",
            },
            "id": 957647,
            "relations": [
                {
                    "attributes": {"isLocked": False, "name": "Child"},
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
                    + "_apis/wit/workItems/957691",
                },
                {
                    "attributes": {"isLocked": False, "name": "Child"},
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
                    + "_apis/wit/workItems/980015",
                },
                {
                    "attributes": {"isLocked": False, "name": "Child"},
                    "rel": "System.LinkTypes.Hierarchy-Forward",
                    "url": "https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
                    + "_apis/wit/workItems/957653",
                },
            ],
            "rev": 197,
        }
    )

    parent = data.lookup(
        "/relations/(/attributes/name=Parent).first/url.split(/).last.int"
    )
    assert parent is None, parent


def test_no_children() -> None:
    """Validate that if there are no children we get the default value"""
    data = DataObject(
        {
            "url": "https://https://dev.azure.com/company/94b22d7b-4f5e-88f0-ad7b-867910f91c94/"
            + "_apis/wit/workItems/2172903/revisions/34",
            "fields": {
                "System.AreaPath": "Project\\Group\\Area\\Product\\Team3",
                "System.TeamProject": "Project",
                "System.IterationPath": "Project",
                "System.WorkItemType": "Technical Debt",
                "System.State": "New",
                "System.Reason": "Moved to state New",
                "System.CreatedDate": "2022-10-04T20:42:34.24Z",
                "System.CreatedBy": {
                    "displayName": "Sarah Smith",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/_apis/Identities/"
                    + "b7197938-6360-ae5e-ea80-b6f0db8a8734",
                    "_links": {
                        "avatar": {
                            "href": "https://https://dev.azure.com/company/_apis/"
                            + "GraphProfile/MemberAvatars/"
                            + "aad.YjcxOTc5MzgtZWE4MC03MzYwLWFlNWUtYjZmMGRiOGE4NzM0"
                        }
                    },
                    "id": "b7197938-6360-ae5e-ea80-b6f0db8a8734",
                    "uniqueName": "user9@company.com",
                    "imageUrl": "https://https://dev.azure.com/company/_apis/"
                    + "GraphProfile/MemberAvatars/"
                    + "aad.YjcxOTc5MzgtZWE4MC03MzYwLWFlNWUtYjZmMGRiOGE4NzM0",
                    "inactive": True,
                    "descriptor": "aad.YjcxOTc5MzgtZWE4MC03MzYwLWFlNWUtYjZmMGRiOGE4NzM0",
                },
                "System.ChangedDate": "2026-05-07T16:20:48.85Z",
                "System.ChangedBy": {
                    "displayName": "David Tennent",
                    "url": "https://spsprodeus24.vssps.visualstudio.com/"
                    + "Afae0922c-42ea-b8cb-6afd-e21a431ec8dd/"
                    + "_apis/Identities/dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "_links": {
                        "avatar": {
                            "href": "https://https://dev.azure.com/company/"
                            + "_apis/GraphProfile/MemberAvatars/"
                            + "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2"
                        }
                    },
                    "id": "dc42cd0e-4553-8516-ab09-9efe930b92a2",
                    "uniqueName": "user12@company.com",
                    "imageUrl": "https://https://dev.azure.com/company/_apis/"
                    + "GraphProfile/MemberAvatars/"
                    + "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                    "descriptor": "aad.YWZkMzg2MTItMTAwMy03YmM1LWI1ODQtMTY1YTcwMmM1MmE2",
                },
                "System.CommentCount": 0,
                "System.Title": "HW test (SOQPSK De-modulator) ",
                "System.BoardColumn": "New",
                "System.BoardColumnDone": False,
                "Microsoft.VSTS.Common.StateChangeDate": "2023-02-03T16:03:30.38Z",
                "Microsoft.VSTS.Common.ValueArea": "Business",
                "Microsoft.VSTS.Common.StackRank": 666666666.0,
                "Microsoft.VSTS.Scheduling.StoryPoints": 2.0,
                "Custom.ParentID": 3019958,
                "Custom.ParentTitle": "HW Testing",
                "WEF_D8499809B15042DAABC202ECF51A67D8_Kanban.Column": "New",
                "WEF_D8499809B15042DAABC202ECF51A67D8_Kanban.Column.Done": False,
                "Custom.AssignedToDate": "2024-09-12T12:01:55Z",
                "Custom.DaysUntilAssigned": 0.0,
                "WEF_EA2D3B3120E248EE9712884AA53DDD51_Kanban.Column": "New",
                "WEF_EA2D3B3120E248EE9712884AA53DDD51_Kanban.Column.Done": False,
                "Custom.WIRLastSeenUpdate": 29,
                "WEF_42B49516479B4AEEA0D80D89E8893C45_Kanban.Column": "New",
                "WEF_42B49516479B4AEEA0D80D89E8893C45_Kanban.Column.Done": False,
                "WEF_D002AFEBFA2949B2852FA37C1C014A8B_Kanban.Column": "New",
                "WEF_D002AFEBFA2949B2852FA37C1C014A8B_Kanban.Column.Done": False,
                "WEF_3E05701FE5EA4460876365252800813A_Kanban.Column": "New",
                "WEF_3E05701FE5EA4460876365252800813A_Kanban.Column.Done": False,
                "System.Description": "<div>Automated testing of the demod example on hardware."
                + " Should exercise every control and test multiple "
                + "starting configurations. </div>",
                "System.Tags": "DLTF",
                "System.Parent": 3019958,
            },
            "id": 2172903,
            "relations": [
                {
                    "attributes": {"isLocked": False, "name": "Related"},
                    "rel": "System.LinkTypes.Related",
                    "url": "https://https://dev.azure.com/company/"
                    + "94b22d7b-4f5e-88f0-ad7b-867910f91c94/_apis/wit/workItems/2522564",
                },
                {
                    "attributes": {"isLocked": False, "name": "Parent"},
                    "rel": "System.LinkTypes.Hierarchy-Reverse",
                    "url": "https://https://dev.azure.com/company/"
                    + "94b22d7b-4f5e-88f0-ad7b-867910f91c94/_apis/wit/workItems/3019958",
                },
            ],
            "rev": 34,
        }
    )

    children = data.lookup(
        "/relations/(/attributes/name=Child)/url.split(/).last.int", []
    )
    assert children == [], children


if __name__ == "__main__":
    test_no_children()
    test_no_parent()
    test_lookup_missing()
    test_lookup()
    test_dataobject_basic()
