#!/usr/bin/env python3


""" Ability to send emails with embedded images """


from smtplib import SMTP as OS_SMTP, SMTP_SSL as OS_SMTP_SSL
from email.mime.multipart import MIMEMultipart as OS_MIMEMultipart
from email.mime.text import MIMEText as OS_MIMEText
from email.mime.image import MIMEImage as OS_MIMEImage

from devopsdriver.settings import Settings


IMAGE_HEADERS = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8\xff"}

# for testing
MIMEMULTIPART = OS_MIMEMultipart
MIMETEXT = OS_MIMEText
MIMEIMAGE = OS_MIMEImage
SMTP = OS_SMTP
SMTPSSL = OS_SMTP_SSL


def image_extension(data: bytes) -> str:
    """Given image data, determine the file extension

    Args:
        data (bytes): The image binary data

    Raises:
        AttributeError: If the data type is not recognized

    Returns:
        str: The extension, like ".png"
    """
    for extension, header in IMAGE_HEADERS.items():
        if data.startswith(header):
            return extension

    raise AttributeError("Image not a known format: " + ",".join(IMAGE_HEADERS))


def send_email(
    recipients: str | list[str],
    subject: str,
    html_body: str,
    settings: Settings = None,
    **image_data,
):
    """Sends an email with embedded images

    Args:
        recipients (str | list[str]): A single email address or a list of them
        subject (str): Subject line
        html_body (str): html formatted body. To reference an image in your
                        body, <img src="cid:image1"> if you pass image1=png.read()
        settings (Settings, optional): The settings object. Defaults to None.
        image_data (dict, optional): keyword image names to binary image data
    """
    settings = Settings(__file__).key("secrets") if settings is None else settings
    required = {"smtp.sender", "smtp.server", "smtp.port", "smtp.password"}
    missing = {r for r in required if r not in settings}
    assert not missing, (
        ", ".join(missing) + " not found in:\n" + "\n".join(settings.search_files)
    )
    sender = settings["smtp.sender"]
    username = settings.get("smtp.username", sender)
    message = MIMEMULTIPART()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(
        [recipients] if isinstance(recipients, str) else recipients
    )
    message.attach(MIMETEXT(html_body, "html"))
    connection_type = SMTPSSL if settings.get("smtp.ssl", True) else SMTP

    for name, binary_data in image_data.items():
        image = MIMEIMAGE(binary_data)
        image.add_header("Content-ID", f"<{name}>")
        image.add_header(
            "Content-Disposition",
            "inline",
            filename=name + image_extension(binary_data),
        )
        message.attach(image)

    with connection_type(settings["smtp.server"], settings["smtp.port"]) as smtp:
        smtp.set_debuglevel(False)
        smtp.login(username, settings["smtp.password"])
        smtp.sendmail(sender, recipients, message.as_string())
        smtp.quit()
