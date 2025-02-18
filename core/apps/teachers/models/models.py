from django.utils.translation import gettext_lazy as _

from core.apps.teachers.models import TeacherManager
from core.apps.users.models import User


class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')
        ordering = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        self.is_teacher = True
        super().save(*args, **kwargs)
