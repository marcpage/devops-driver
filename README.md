![status sheild](https://img.shields.io/static/v1?label=status&message=beta&color=blue&style=plastic)
[![status sheild](https://img.shields.io/static/v1?label=released&message=v0.1.40&color=active&style=plastic)](https://pypi.org/project/devopsdriver/0.1.40/)
[![GitHub](https://img.shields.io/github/license/marcpage/devops-driver?style=plastic)](https://github.com/marcpage/devops-driver?tab=Unlicense-1-ov-file#readme)
[![GitHub contributors](https://img.shields.io/github/contributors/marcpage/devops-driver?style=flat)](https://github.com/marcpage/devops-driver/graphs/contributors)
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)

[![commit sheild](https://img.shields.io/github/last-commit/marcpage/devops-driver?style=plastic)](https://github.com/marcpage/devops-driver/commits)
[![activity sheild](https://img.shields.io/github/commit-activity/m/marcpage/devops-driver?style=plastic)](https://github.com/marcpage/devops-driver/commits)
[![GitHub top language](https://img.shields.io/github/languages/top/marcpage/devops-driver?style=plastic)](https://github.com/marcpage/devops-driver)
[![size sheild](https://img.shields.io/github/languages/code-size/marcpage/devops-driver?style=plastic)](https://github.com/marcpage/devops-driver)

[![example workflow](https://github.com/marcpage/devops-driver/actions/workflows/pr.yml/badge.svg)](https://github.com/marcpage/devops-driver/actions/workflows/pr.yml)
[![status sheild](https://img.shields.io/static/v1?label=test+coverage&message=99%&color=active&style=plastic)](https://github.com/marcpage/devops-driver/blob/main/Makefile#L4)
[![issues sheild](https://img.shields.io/github/issues-raw/marcpage/devops-driver?style=plastic)](https://github.com/marcpage/devops-driver/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/marcpage/devops-driver?style=flat)](https://github.com/marcpage/devops-driver/pulls)

[![follow sheild](https://img.shields.io/github/followers/marcpage?label=Follow&style=social)](https://github.com/marcpage?tab=followers)
[![watch sheild](https://img.shields.io/github/watchers/marcpage/devops-driver?label=Watch&style=social)](https://github.com/marcpage/devops-driver/watchers)

[![Python](https://img.shields.io/static/v1?label=&message=Pure%20Python&color=ffde57&style=plastic&logo=python)](https://python.org/)
[![Azure](https://img.shields.io/static/v1?label=&message=Supports%20Microsoft%20Azure&color=blue&style=plastic&logo=microsoftazure)](https://azure.microsoft.com/)
[![Gmail](https://img.shields.io/static/v1?label=&message=Supports%20Google%20Gmail&color=white&style=plastic&logo=gmail)](https://gmail.com/)

OS: 
[![Windows](https://img.shields.io/static/v1?label=&message=Windows&color=blue&style=plastic&logo=windows)](https://microsoft.com/)
[![macOS](https://img.shields.io/static/v1?label=&message=macOS&color=white&logoColor=black&style=plastic&logo=apple)](https://apple.com/)
[![Linux](https://img.shields.io/static/v1?label=&message=Linux&color=seashell&logoColor=black&style=plastic&logo=linux)](https://linux.org/)

# devops-driver

Devops-driver is a collection of tools to help streamline developer's experience and gain insights into various processes.

## Tools

devopsdriver is a toolbox that helps to quickly put together reports. Some of the items in the toolbox are:

- **Settings**: store data, constants, settings, keys, tokens, etc. both in and out of the repository
- **send_email**: send emails over SMTP (including SSL), using `Settings` to store credentials
- **Template**: Simplify generating reports using `.mako` templates
- **Azure.workitem**: Search for and inspect Azure DevOps work items

## Example use-case

To allow seamless work in both pipelines as well as in the development environment, the `Settings` object gives you access to common settings among multiple scripts, secrets, and configuration constants in a way the helps keep secrets out of the repository but runs just as well in the pipeline as your machine.

Say you want a pipeline that looks for User Stories that are newer than 3 days and send out an email.

### \<platform dependent path\>/devopsdriver.yml
```yaml
smtp:
    sender: JohnDoe@company.com

secrets:
    azure.token: azure/token
    smtp.password: smtp/password
```

This file is in a global place (location varies by OS) and stores information that you may not want in your repository or is specific to development. 

| Platform | Global Directory       |
|----------|------------------------|
| Windows  | %APPDATA%\             |
| Linux    | ~/.devopsdriver/       |
| macOS    | ~/Library/Preferences/ |

The `secrets` are extra sensative and are stored in the OS keychain.

### Set secrets in the keychain
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install devopsdriver
$ settings --secrets
secret: smtp.password  key: smtp/password
smtp.password (smtp/password): ****
secret: azure.token  key: azure/token
smtp.password (azure/token): ****
$ settings --secrets
secret: azure.token  key: azure/token
	Value set
secret: smtp.password  key: smtp/password
	Value set
$
```
The first call to `settings` will look for every secret and check if they are already set in the keychain.
For any secret that has not been set in the keychain, you will be prompted to enter the password to store.
The second call to `settings` will verify that all the values have been set in the keychain.

### devopsdriver.yml
```yaml
azure:
    url: https://dev.azure.com/MyCompany

smtp:
    server: smtp.company.com
    port: 465

cli:
    azure.token: --azure-token
    smtp.password: --smtp-password
    smtp.sender: --smtp-sender

env:
    azure.token: AZURE_TOKEN
    smtp.sender: SMTP_SENDER
    smtp.password: SMTP_PASSWORD
```

This file lives next to your scripts in your repository.
These are settings that would be used by everyone, including the pipeline.
The `cli` and `env` map command line switches and environment variables to those keys.
This allows for many options for setting values depending on your needs.

### new_stories.yml
```yaml
scrum masters:
    - JohnDoe@company.com
    - JaneDoe@company.com
```
This file is specific to your script and not shared.
These are values that you want to use in your script but have them here for easy adjustment.

### new_stories.html.mako
```html
<h1>Stories created in the last ${days} days</h1>
<ul>
    % for story in stories:
    <li>${story.id} ${story.title}</li>
    % endfor
</ul>
```

This file is the template for the email body.

### new_stories.py
```python
from datetime import date, timedelta

from devopsdriver import Settings, Azure, send_email, Template
from devopsdriver.azdo import Wiql, GreaterThan

# Parse all the settings from files, command line, environment, and keychain
settings = Settings(__file__).key("secrets").cli("cli").env("env")

# Create connection to Azure Devops
azure = Azure(settings)

# Get User Stories created in the last three days
three_days_ago = date.today() - timedelta(days=settings["days of recent stories"])
new_stories = azure.workitem.find(
    Wiql().where(GreaterThan("CreatedDate", three_days_ago))
)

# Generate html body of the email
message = Template(__file__).render(
    days=settings["days of recent stories"],
    stories=new_stories,
)

# Send the email
send_email(
    recipients=settings["scrum masters"],
    subject=f'Stories created in the last {settings["days of recent stories"]} days',
    html_body=message,
    settings=settings,
)
```

### The email sent

**From**: JohnDoe@company.com

**To**: JohnDoe@company.com, JaneDoe@company.com

**Subject**: Stories created in the last 3 days

#### Stories created in the last 3 days

- 745 Needs a preprocessing step that makes it case insensitive
- 749 Create GitHub action to automate process
- 750 Create GitHub action to automate process
- 751 Test
- 752 Feedback Capture
- 753 draft doc history retrieval method
- 754 frontend - store to schema
- 755 Transfer job to production. Setup migrations to move to production
- 756 Query subscription status from App

