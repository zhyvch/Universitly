from django.conf import settings
from django.db import transaction

from core.apps.education.models import Institution
from core.apps.education.selectors import DjangoORMInstitutionSelector
from core.apps.tasks.models import Email
from core.apps.tasks.tasks import send_email

class DjangoORMInstitutionService:
    selector = DjangoORMInstitutionSelector()

    @transaction.atomic
    def create_institution(
            self,
            owner: settings.AUTH_USER_MODEL,
            title: str,
            type: str | None = None,
            icon: str | None = None,
    ) -> Institution:
        institution = Institution()
        institution.owner = owner
        institution.title = title
        if type:
            institution.type = type
        if icon:
            institution.icon = icon
        institution.full_clean()
        institution.save()

        send_email.apply_async_on_commit(kwargs={
            'email_type': Email.EmailType.CREATING_INSTITUTION,
            'to': owner.email,
            'name': owner.get_full_name() or owner.email[:owner.email.index('@')],
            'institution': institution.title,
        })

        return institution

    @transaction.atomic
    def update_institution(
            self,
            owner: settings.AUTH_USER_MODEL,
            institution_id: int,
            title: str | None = None,
            type: str | None = None,
            icon: str | None = None,
    ) -> Institution:
        if not self.selector.validate_ownership(owner_id=owner.id, institution_id=institution_id):
            raise

        institution = self.selector.get_institution_by_id(institution_id)
        changes_log = ''
        if title:
            changes_log+=f'\nChanged title from "{institution.title}" to "{title}"'
            institution.title = title
        if type:
            changes_log+=f'\nChanged type from "{institution.type}" to "{type}"'
            institution.type = type
        if icon:
            changes_log+=f'\nChanged icon from "{institution.icon}" to "{icon}"'
            institution.icon = icon
        institution.full_clean()
        institution.save()

        send_email.apply_async_on_commit(kwargs={
            'email_type': Email.EmailType.UPDATING_INSTITUTION,
            'to': owner.email,
            'name': owner.get_full_name() or owner.email[:owner.email.index('@')],
            'institution': institution.title,
            'changes': changes_log
        })

        return institution

    @transaction.atomic
    def delete_institution(
            self,
            owner: settings.AUTH_USER_MODEL,
            institution_id: int,
    ) -> None:
        if not self.selector.validate_ownership(owner_id=owner.id, institution_id=institution_id):
            raise

        institution = self.selector.get_institution_by_id(institution_id)
        institution.delete()

        send_email.apply_async_on_commit(kwargs={
            'email_type': Email.EmailType.DELETING_INSTITUTION,
            'to': owner.email,
            'name': owner.get_full_name() or owner.email[:owner.email.index('@')],
            'institution': institution.title,
        })
