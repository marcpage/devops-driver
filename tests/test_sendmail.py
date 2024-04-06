#!/usr/bin/env python3

""" Test sendmail """

from devopsdriver import sendmail  # for debugging
from devopsdriver.sendmail import send_email


class MockMultipart(dict):
    """Mock mime multipart"""

    def __init__(self):
        self.objects = []
        super().__init__()

    def attach(self, thing):
        """mock attaching"""
        self.objects.append(thing)

    def as_string(self) -> str:
        """don't actually convert to string so we can check fields"""
        return self


class MockText:
    """mock mime text"""

    def __init__(self, text: str, kind: str):
        self.text = text
        self.kind = kind


class MockImage:
    """mock mime image"""

    def __init__(self, data: bytes):
        self.data = data
        self.headers = {}
        self.filenames = {}

    def add_header(self, key, value, filename=None):
        """store headers and filenames (if they have them)"""
        self.headers[key] = value

        if filename:
            self.filenames[key] = filename


class MockSmtp:
    """mock smtp and smpt_ssl"""

    def __init__(self, server: str, port: int):
        self.server = server
        self.port = port
        self.debuglevel = None
        self.username = None
        self.password = None
        self.sender = None
        self.recipients = None
        self.message = None

    def set_debuglevel(self, level: bool):
        """store that we've set the debug level"""
        self.debuglevel = level

    def login(self, username: str, password: str):
        """store the credentials"""
        self.username = username
        self.password = password

    def sendmail(self, sender: str, recipients: list[str], message: str):
        """store what we're sending"""
        self.sender = sender
        self.recipients = recipients
        self.message = message

    def quit(self):
        """on quit check everything"""
        assert self.server == "smtp.com", self.server
        assert self.port == 1234, self.port
        assert not self.debuglevel and self.debuglevel is not None, self.debuglevel
        assert self.username == "from@domain.com", self.username
        assert self.password == "setec astronomy", self.password
        assert self.sender == "from@domain.com", self.sender
        assert self.recipients == "to@domain.com", self.recipients
        assert len(self.message.objects) == 2, self.message.objects
        assert self.message.objects[0].text == "body", self.message.objects[0].text
        assert self.message.objects[0].kind == "html", self.message.objects[0].kind
        assert (
            self.message.objects[1].data == b"\x89PNG\r\n\x1a\n0000"
        ), self.message.objects[1].data
        assert (
            self.message.objects[1].headers["Content-ID"] == "<image1>"
        ), self.message.objects[1].headers["Content-ID"]
        assert (
            self.message.objects[1].headers["Content-Disposition"] == "inline"
        ), self.message.objects[1].headers["Content-Disposition"]
        assert (
            self.message.objects[1].filenames["Content-Disposition"] == "image1.png"
        ), self.message.objects[1].filenames["Content-Disposition"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


def test_basic() -> None:
    """test basics"""
    sendmail.MIMEMULTIPART = MockMultipart
    sendmail.MIMETEXT = MockText
    sendmail.MIMEIMAGE = MockImage
    sendmail.SMTP = MockSmtp
    sendmail.SMTPSSL = MockSmtp
    settings = {
        "smtp.sender": "from@domain.com",
        "smtp.server": "smtp.com",
        "smtp.port": 1234,
        "smtp.password": "setec astronomy",
    }
    send_email(
        "to@domain.com", "subject", "body", settings, image1=b"\x89PNG\r\n\x1a\n0000"
    )


def test_unknown_image_type() -> None:
    """test basics"""
    sendmail.MIMEMULTIPART = MockMultipart
    sendmail.MIMETEXT = MockText
    sendmail.MIMEIMAGE = MockImage
    sendmail.SMTP = MockSmtp
    sendmail.SMTPSSL = MockSmtp
    settings = {
        "smtp.sender": "from@domain.com",
        "smtp.server": "smtp.com",
        "smtp.port": 1234,
        "smtp.password": "setec astronomy",
    }

    try:
        send_email("to@domain.com", "subject", "body", settings, image1=b"bwahaha")
        raise AssertionError("We should have thrown")

    except AttributeError:
        pass


if __name__ == "__main__":
    test_unknown_image_type()
    test_basic()
