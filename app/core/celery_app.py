from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "app",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_routes={"app.tasks.email.*": {"queue": "emails"}},
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)
celery_app.autodiscover_tasks(["app.tasks"])
celery_app.set_default()

import app.tasks.email  # noqa: E402,F401
