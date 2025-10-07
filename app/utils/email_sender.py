import ssl
from abc import ABC, abstractmethod
from email.message import EmailMessage

import certifi
from aiosmtplib import send

from app.core.config import settings

_TLS_CTX = ssl.create_default_context(cafile=certifi.where())


class BaseMessenger(ABC):
    @abstractmethod
    def send_letter(self, to: str, text: str) -> None:
        raise NotImplementedError


class Messenger(BaseMessenger):
    def __init__(self):
        self._smtp_config = {
            "hostname": settings.SMTP_HOST,
            "port": settings.SMTP_PORT,
            "start_tls": True,
            "use_tls": False,
            "username": settings.SMTP_USERNAME,
            "password": settings.SMTP_PASSWORD,
        }

    async def send_letter(self, to_email: str, text: str, subject: str = "Message"):
        msg = EmailMessage()
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(text)

        await send(msg, tls_context=_TLS_CTX, **self._smtp_config)
