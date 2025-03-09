from typing import TypeVar

from django.db.models import QuerySet

from core.apps.education.models import Institution

IT = TypeVar('IT', bound=Institution)


class DjangoORMInstitutionSelector[IT]:
    model: type[IT] = Institution

    def get_institution_list(self) -> QuerySet[IT]:
        return self.model.objects.all()

    def get_institution_by_id(self, institution_id: int) -> IT:
        return self.model.objects.get(id=institution_id)
