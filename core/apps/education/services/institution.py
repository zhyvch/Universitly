from django.db import transaction

from core.apps.education.models import Institution
from core.apps.education.selectors import DjangoORMInstitutionSelector, IT
from core.apps.users.selectors import UT
from core.apps.tasks.models import Email
from core.apps.tasks.tasks import send_email


class DjangoORMInstitutionService[IT, UT]:
    selector = DjangoORMInstitutionSelector()

    @transaction.atomic
    def create_institution(
            self,
            user: UT,
            title: str,
            type: str | None = None,
            icon: str | None = None,
    ) -> IT:
        institution = Institution()
        institution.owner = user
        institution.title = title
        if type:
            institution.type = type
        if icon:
            institution.icon = icon
        institution.full_clean()
        institution.save()

        send_email.apply_async_on_commit(kwargs={
            'email_type': Email.EmailType.CREATING_INSTITUTION,
            'to': user.email,
            'name': user.full_name or user.email_username,
            'institution': institution.title,
        })

        return institution

    @transaction.atomic
    def update_institution(
            self,
            user: UT,
            institution_id: int,
            title: str | None = None,
            type: str | None = None,
            icon: str | None = None,
    ) -> IT:
        try:
            institution = self.selector.get_institution_by_id(institution_id)
        except Institution.DoesNotExist:
            raise

        if not institution.is_owner(user.id):
            raise

        institution = self.selector.get_institution_by_id(institution_id)
        changes_log = ''
        if title:
            changes_log += f'\nChanged title from "{institution.title}" to "{title}"'
            institution.title = title
        if type:
            changes_log += f'\nChanged type from "{institution.type}" to "{type}"'
            institution.type = type
        if icon:
            changes_log += f'\nChanged icon from "{institution.icon}" to "{icon}"'
            institution.icon = icon
        institution.full_clean()
        institution.save()
        send_email.apply_async_on_commit(kwargs={
            'email_type': Email.EmailType.UPDATING_INSTITUTION,
            'to': user.email,
            'name': user.full_name or user.email_username,
            'institution': institution.title,
            'changes': changes_log
        })

        return institution

    @transaction.atomic
    def delete_institution(
            self,
            user: UT,
            institution_id: int,
    ) -> None:
        try:
            institution = self.selector.get_institution_by_id(institution_id)
        except Institution.DoesNotExist:
            raise

        if not institution.is_owner(user.id):
            raise

        institution.delete()

        send_email.apply_async_on_commit(kwargs={
            'email_type': Email.EmailType.DELETING_INSTITUTION,
            'to': user.email,
            'name': user.full_name or user.email_username,
            'institution': institution.title,
        })
