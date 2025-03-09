from django.db import transaction

from core.apps.education.selectors import DjangoORMCourseSelector, CT
from core.apps.users.selectors import UT

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
