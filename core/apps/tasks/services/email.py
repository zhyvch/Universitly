from typing import Iterable

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

from core.apps.tasks.models import Email
from core.apps.tasks.selectors import DjangoORMEmailSelector


class DjangoORMEmailService:
    selector = DjangoORMEmailSelector()

    def send_email(self, email_type: Email.EmailType, to: str, **kwargs) -> bool:
        email = self.selector.get_email_by_type(email_type)
        message = EmailMultiAlternatives(
            subject=email.subject,
            body=email.plain_text % kwargs,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to],
        )
        message.attach_alternative(email.html % kwargs, 'text/html')

        return bool(message.send())

    def send_mass_mail(self, email_type: Email.EmailType, to: Iterable[str], **kwargs) -> int:
        email = self.selector.get_email_by_type(email_type)
        messages = [
            EmailMultiAlternatives(
                subject=email.subject,
                body=email.plain_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[address],
                alternatives=[(email.html, 'text/html')],
            ) for address in to
        ]
        connection = get_connection()

        return connection.send_messages(messages)
