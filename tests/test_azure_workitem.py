#!/usr/bin/env python3

""" Test work item """

from devopsdriver.azure import WorkItem


class MockAzureWorkItem:
    """mock out work item"""

    def as_dict(self):
        """mock out as_dict"""
        return {
            "id": 5,
            "rev": 1,
            "url": "https://dev.azure.com/MyOrg/faf4b2ab-a8b4-4ab8-bca8-6f1f63fe6a91/"
            + "_apis/wit/workItems/5/revisions/1",
            "fields": {
                "System.WorkItemType": "User Story",
                "System.State": "New",
                "System.Reason": "New",
                "System.CreatedDate": "2023-11-16T03:12:32.94Z",
                "System.CreatedBy": {
                    "displayName": "Edna Johnson",
                    "url": "https://spsprodcus5.vssps.visualstudio.com/"
                    + "A3eb27a26-75f2-40f9-87dc-cc10e8e565e4/_apis/Identities"
                    + "/45fcf770-0670-69d4-8e48-3ae6e0bf9b5c",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/MyOrg/_apis/GraphProfile/"
                            + "MemberAvatars/aad.NDVmY2Y3NzAtMDY3MC03OWQ0LThlNDgtM2FlNmUwYmY5YjVj"
                        }
                    },
                    "id": "45fcf770-0670-69d4-8e48-3ae6e0bf9b5c",
                    "uniqueName": "edna@company.com",
                    "imageUrl": "https://dev.azure.com/MyOrg/_apis/GraphProfile/"
                    + "MemberAvatars/aad.NDVmY2Y3NzAtMDY3MC03OWQ0LThlNDgtM2FlNmUwYmY5YjVj",
                    "inactive": True,
                    "descriptor": "aad.NDVmY2Y3NzAtMDY3MC03OWQ0LThlNDgtM2FlNmUwYmY5YjVj",
                },
                "System.ChangedDate": "2023-11-16T03:12:32.94Z",
                "System.ChangedBy": {
                    "displayName": "Edna Johnson",
                    "url": "https://spsprodcus5.vssps.visualstudio.com/"
                    + "A3eb27a26-75f2-40f9-87dc-cc10e8e565e4/_apis/Identities/"
                    + "45fcf770-0670-69d4-8e48-3ae6e0bf9b5c",
                    "_links": {
                        "avatar": {
                            "href": "https://dev.azure.com/MyOrg/_apis/GraphProfile/"
                            + "MemberAvatars/aad.NDVmY2Y3NzAtMDY3MC03OWQ0LThlNDgtM2FlNmUwYmY5YjVj"
                        }
                    },
                    "id": "45fcf770-0670-69d4-8e48-3ae6e0bf9b5c",
                    "uniqueName": "edna@company.com",
                    "imageUrl": "https://dev.azure.com/MyOrg/_apis/GraphProfile/"
                    + "MemberAvatars/aad.NDVmY2Y3NzAtMDY3MC03OWQ0LThlNDgtM2FlNmUwYmY5YjVj",
                    "inactive": True,
                    "descriptor": "aad.NDVmY2Y3NzAtMDY3MC03OWQ0LThlNDgtM2FlNmUwYmY5YjVj",
                },
                "System.CommentCount": 0,
                "System.TeamProject": "Creative",
                "System.AreaPath": "Creative",
                "System.IterationPath": "Creative\\November 2 2023",
                "System.Title": "test",
                "Microsoft.VSTS.Common.Priority": 2,
                "Microsoft.VSTS.Common.ValueArea": "Business",
                "WEF_FBFB2B85F9CD4A7C9AA907EBB29D5863_Kanban.Column": "To Do",
                "WEF_FBFB2B85F9CD4A7C9AA907EBB29D5863_Kanban.Column.Done": False,
                "System.BoardColumn": "To Do",
                "System.BoardColumnDone": False,
                "Microsoft.VSTS.Common.StateChangeDate": "2023-11-16T03:12:32.94Z",
            },
        }


def test_workitem() -> None:
    """test basic work item"""
    wi = WorkItem(MockAzureWorkItem())
    assert wi.id == 5, wi.id
    assert wi.ID == 5, wi.ID
    assert wi.workitemtype == "User Story", wi.workitemtype
    assert wi.system_workitemtype == "User Story", wi.system_workitemtype
    assert wi.ChangedBy["displayName"] == "Edna Johnson", wi.changedBy
    assert wi.changedby.displayname == "Edna Johnson", wi.changedby.displayname
    assert wi.microsoft_vsts_common_priority == 2, wi.microsoft_vsts_common_priority

    try:
        _ = wi.not_a_field

    except AttributeError as error:
        assert "not_a_field" in str(error)


if __name__ == "__main__":
    test_workitem()