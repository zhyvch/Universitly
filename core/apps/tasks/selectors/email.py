from core.apps.tasks.models import Email


class DjangoORMEmailSelector:
    model = Email

    def get_email_by_type(self, email_type: Email.EmailType) -> model:
        return self.model.objects.get(type=email_type)
