from typing import Iterable

from core.apps.education.models import Institution


class DjangoORMInstitutionSelector:
    model = Institution

    def get_institution_list(self) -> Iterable[model]:
        return self.model.objects.all()

    def get_institution_by_id(self, institution_id) -> model:
        return self.model.objects.get(id=institution_id)

    def validate_ownership(self, owner_id: int, institution_id: int) -> bool:
        return self.model.objects.filter(owner_id=owner_id, id=institution_id).exists()
