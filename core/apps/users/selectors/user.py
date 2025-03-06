from typing import Iterable

from django.contrib.auth import get_user_model


class DjangoORMUserSelector:
    model = get_user_model()

    def get_active_users(self) -> Iterable[model]:
        return self.model.objects.filter(is_active=True)
