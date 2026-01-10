import logging

from fastapi import APIRouter, HTTPException

from app.schemas import EmailRequest
from app.services.email_service import send_email

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/send-email")
async def send_email_endpoint(email_request: EmailRequest) -> dict[str, str]:
    """
    Endpoint to send an anonymous email.
    """
    try:
        await send_email(
            recipient=email_request.recipient,
            subject=email_request.subject,
            message=email_request.message,
        )
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")