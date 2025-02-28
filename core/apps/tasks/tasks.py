from celery import shared_task
from celery.utils.log import get_task_logger

from core.apps.tasks.models import Email
from core.apps.tasks.services import EmailService

logger = get_task_logger(__name__)

@shared_task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task(bind=True)
def send_email(self, type: Email.EmailType, to: str):
    service = EmailService()

    try:
        return service.send_email(email_type=type, to=to)
    except Exception as e:
        logger.error(f'Error sending email: {e}')
        self.retry(exc=e, countdown=5)

