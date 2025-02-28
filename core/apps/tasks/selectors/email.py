from core.apps.tasks.models import Email


class EmailSelector:
    @staticmethod
    def get_email(email_type: Email.EmailType) -> Email:
        return Email.objects.get(type=email_type)
