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

        # Determine TLS mode based on port
        # Port 465: Implicit TLS (use_tls=True, start_tls=False)
        # Port 587: STARTTLS (use_tls=False, start_tls=True)
        is_starttls = settings.SMTP_PORT == 587

        logger.info(f"Connecting to SMTP server {settings.SMTP_SERVER}:{settings.SMTP_PORT} (STARTTLS={is_starttls})...")

        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            use_tls=not is_starttls,
            start_tls=is_starttls,
            timeout=settings.SMTP_TIMEOUT,
        )

        logger.info(f"Email sent successfully to {recipient}")

    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
        raise e