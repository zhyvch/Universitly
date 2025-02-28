from typing import Iterable

from core.apps.education.models import Institution


class DjangoORMInstitutionSelector:
    @staticmethod
    def get_institution_list() -> Iterable[Institution]:
        return Institution.objects.all()

    @staticmethod
    def get_institution_by_id(institution_id) -> Institution:
        return Institution.objects.get(id=institution_id)

    @staticmethod
    def validate_ownership(owner_id: int, institution_id: int) -> bool:
        return Institution.objects.filter(owner_id=owner_id, id=institution_id).exists()
