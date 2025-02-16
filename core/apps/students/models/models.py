from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.common.models import TimestampedBaseModel
from core.apps.courses.models import SectionTest
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


class SectionTestAttempt(TimestampedBaseModel):
    student = models.ForeignKey(
        verbose_name=_('Student'),
        to=Student,
        on_delete=models.SET_NULL,
        null=True
    )
    test = models.ForeignKey(
        verbose_name=_('Attempted test'),
        to=SectionTest,
        on_delete=models.CASCADE
    )
    score = models.FloatField(
        verbose_name=_('Score'),
        default=0
    )

    @property
    def is_passing(self):
        return self.score >= self.test.passing_score

    @property
    def letter_grade(self):
        return self.test.get_letter_grade(self.score)

    @property
    def attempts_left(self):
        return self.test.max_attempts - self.objects.filter(student=self.student, test=self.test).count()

    @property
    def can_attempt(self): # strange function, maybe move to selector
        return self.attempts_left > 0 and self.test.is_open

    class Meta:
        verbose_name = _('Section test attempt')
        verbose_name_plural = _('Section test attempts')
