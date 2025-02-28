from collections.abc import Sequence

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

from core.apps.tasks.models import Email
from core.apps.tasks.selectors import EmailSelector


class EmailService:
    selector = EmailSelector

    def send_email(self, email_type: Email.EmailType, to: str) -> bool:
        email = self.selector.get_email(email_type)
        message = EmailMultiAlternatives(
            subject=email.subject,
            body=email.plain_text,
            from_email=settings.EMAIL_HOST_USER,
            to=[to],
        )
        message.attach_alternative(email.html, 'text/html')

        return bool(message.send())

    def send_mass_mail(self, email_type: Email.EmailType, to: Sequence[str]) -> int:
        email = self.selector.get_email(email_type)
        messages = [
            EmailMultiAlternatives(
                subject=email.subject,
                body=email.plain_text,
                from_email=settings.EMAIL_HOST_USER,
                to=address,
                alternatives=[(email.html, 'text/html')],
            ) for address in to
        ]
        connection = get_connection()

        return connection.send_messages(messages)


