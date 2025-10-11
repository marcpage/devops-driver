"""DevOps tools"""

from .settings import Settings
from .sendmail import send_email
from .template import Template
from .azdo.clients import Azure
from .github.client import Github


__version__ = "0.1.52"
__author__ = "Marc Page"
__credits__ = ""
