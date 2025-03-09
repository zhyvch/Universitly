from typing import TypeVar

from core.apps.tasks.models import Email


ET = TypeVar('ET', bound=Email)


class DjangoORMEmailSelector[ET]:
    model: type[ET] = Email

    def get_email_by_type(self, email_type: Email.EmailType) -> ET:
        return self.model.objects.get(type=email_type)
