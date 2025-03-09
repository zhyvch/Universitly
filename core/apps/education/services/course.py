from typing import TypeVar

from django.contrib.auth import get_user_model
from django.db import transaction

from core.apps.education.selectors import DjangoORMCourseSelector


UT = TypeVar('UT', bound=get_user_model())

class DjangoORMCourseService[UT, CT]:
    selector = DjangoORMCourseSelector()

    @transaction.atomic
    def create_course(
            self,
            user: UT,
            institution_id: int,
            title: str,
            teachers: list[int],
            students: list[int],
    ) -> CT:
        ...
