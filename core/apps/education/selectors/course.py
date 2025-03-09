from typing import TypeVar

from django.db.models import QuerySet, Q

from core.apps.education.models import Course

CT = TypeVar('CT', bound=Course)


class DjangoORMCourseSelector[CT]:
    model: type[CT] = Course

    def get_course_list(self, user_id: int, institution_id: int) -> QuerySet[CT]:
        courses = self.model.objects.filter(institution_id=institution_id)

        if not courses.exists():
            return courses

        if courses.exists() and not courses.filter(
            Q(teachers__id=user_id) |
            Q(students__id=user_id) |
            Q(institution__owner_id=user_id)
        ).exists():
            raise

        return courses

    def get_course_by_id(self, course_id) -> CT:
        ...