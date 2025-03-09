from typing import TypeVar

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

UT = TypeVar('UT', bound=get_user_model())


class DjangoORMUserSelector[UT]:
    model: type[UT] = get_user_model()

    def get_active_users(self) -> QuerySet[UT]:
        return self.model.objects.filter(is_active=True)
