from celery import shared_task
from celery.utils.log import get_task_logger

from core.apps.tasks.models import Email
from core.apps.tasks.services import DjangoORMEmailService
from core.apps.users.services import DjangoORMUserService

logger = get_task_logger(__name__)


@shared_task(bind=True)
def send_email(self, email_type: Email.EmailType, to: str, **kwargs):
    service = DjangoORMEmailService()

    try:
        return service.send_email(email_type=email_type, to=to, **kwargs)
    except Exception as e:
        logger.error(f'Error sending email: {e}')
        self.retry(exc=e, countdown=5)


@shared_task(bind=True)
def send_weekly_emails(self, email_type: Email.EmailType):
    email_service = DjangoORMEmailService()
    user_service = DjangoORMUserService()

    try:
        active_users = user_service.selector.get_active_users()

        if not active_users:
            logger.warning('No active users found to send emails')
            return 0

        sent_count = email_service.send_mass_mail(
            email_type=email_type,
            to=active_users.values_list('email', flat=True),
            names=[user.full_name or user.email_username for user in active_users],
        )
        logger.info(f'Successfully sent {sent_count} weekly emails')
        return sent_count
    except Exception as e:
        logger.error(f'Error sending weekly emails: {e}')
        self.retry(exc=e, countdown=60)

