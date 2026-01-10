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

        # Port 465 uses implicit TLS (use_tls=True)
        # Port 587 uses STARTTLS (start_tls=True)
        use_implicit_tls = settings.SMTP_PORT == 465
        use_starttls = settings.SMTP_PORT == 587

        logger.info(f"Connecting to SMTP server {settings.SMTP_SERVER}:{settings.SMTP_PORT} (Implicit TLS={use_implicit_tls}, STARTTLS={use_starttls})...")

        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            use_tls=use_implicit_tls,
            start_tls=use_starttls,
            timeout=settings.SMTP_TIMEOUT,
        )

        logger.info(f"Email sent successfully to {recipient}")

    except Exception as e:
        logger.error(f"Failed to send email to {recipient} via {settings.SMTP_SERVER}:{settings.SMTP_PORT}. Error: {e}")
        raise e