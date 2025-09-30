"""DevOps tools"""

from .settings import Settings
from .sendmail import send_email
from .template import Template
from .azdo.clients import Azure
from .github.github import Github


__version__ = "0.1.50"
__author__ = "Marc Page"
__credits__ = ""
