from django.utils.translation import gettext_lazy as _

from core.apps.students.models import StudentManager
from core.apps.users.models import User


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def save(self, *args, **kwargs):
        self.is_student = True
        super().save(*args, **kwargs)
