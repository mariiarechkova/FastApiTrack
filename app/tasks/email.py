import asyncio
from typing import Optional

from app.core.celery_app import celery_app
from app.utils.email_sender import Messenger


@celery_app.task(
    queue="emails",
    name="app.tasks.email.send_welcome_email",
)
def send_welcome_email(to_email: str, user_name: Optional[str] = None) -> dict:

    who = user_name or to_email
    subject = "Welcome!"
    text = f"Hello, {who}! Welcome on our app."
    asyncio.run(Messenger().send_letter(to_email=to_email, subject=subject, text=text))
    return {"email": to_email, "status": "sent"}
