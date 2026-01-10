import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_email(recipient: str, subject: str, message: str) -> None:
    """
    Sends an email to the specified recipient asynchronously.
    """
    if settings.MOCK_EMAIL:
        logger.info("--- MOCK EMAIL ---")
        logger.info(f"From: {settings.SMTP_FROM_EMAIL}")
        logger.info(f"To: {recipient}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Message: {message}")
        logger.info("------------------")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject

        body = (
            f"You have received an anonymous message:\n\n"
            f"{message}\n\n"
            f"--\n{settings.EMAIL_FOOTER}"
        )
        msg.attach(MIMEText(body, "plain"))

        use_tls = settings.SMTP_PORT == 587

        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            use_tls=not use_tls,
            start_tls=use_tls,
        )

        logger.info(f"Email sent successfully to {recipient}")

    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
        raise e