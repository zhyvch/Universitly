from typing import Optional

from django.db import transaction

from core.apps.education.models import Institution
from core.apps.education.selectors import DjangoORMInstitutionSelector


class DjangoORMInstitutionService:
    selector = DjangoORMInstitutionSelector

    @transaction.atomic
    def create_institution(self,
            owner_id: int,
            title: str,
            type: Optional[str] = None,
            icon: Optional[str] = None,
    ) -> Institution:
        institution = Institution()
        institution.owner_id = owner_id
        institution.title = title
        if type:
            institution.type = type
        if icon:
            institution.icon = icon
        institution.full_clean()
        institution.save()

        return institution

    @transaction.atomic
    def update_institution(
            self,
            institution_id: int,
            title: Optional[str] = None,
            type: Optional[str] = None,
            icon: Optional[str] = None,
    ) -> Institution:
        institution = self.selector.get_institution_by_id(institution_id)
        if title:
            institution.title = title
        if type:
            institution.type = type
        if icon:
            institution.icon = icon
        institution.full_clean()
        institution.save()

        return institution

    @transaction.atomic
    def delete_institution(self, institution_id: int) -> None:
        institution = self.selector.get_institution_by_id(institution_id)
        institution.delete()

