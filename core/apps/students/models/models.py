from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.common.models import TimestampedBaseModel
from core.apps.education.models import SectionTest, SectionHomework
from core.apps.students.models import StudentManager
from core.apps.users.models import User


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['first_name', 'last_name']


class StudentHomework(TimestampedBaseModel):
    student = models.ForeignKey(
        verbose_name=_('Student'),
        to=Student,
        on_delete=models.CASCADE,
        related_name='homeworks',
    )
    section_homework = models.ForeignKey(
        verbose_name=_('Related test'),
        to=SectionHomework,
        on_delete=models.CASCADE,
        related_name='homeworks',
    )

    @property
    def is_late(self):
        return self.updated_at > self.section_homework.deadline

    @property
    def number_of_files(self):
        return self.files.count()

    class Meta:
        verbose_name = _('Student homework')
        verbose_name_plural = _('Student homeworks')


class StudentHomeworkFile(models.Model):
    homework = models.ForeignKey(
        verbose_name=_('Related homework'),
        to=StudentHomework,
        on_delete=models.CASCADE,
        related_name='files',
    )
    file = models.FileField(
        verbose_name=_('File'),
        upload_to='homework_files/',
    )

    class Meta:
        verbose_name = _('Student homework file')
        verbose_name_plural = _('Student homework files')


class StudentTestAttempt(TimestampedBaseModel):
    student = models.ForeignKey(
        verbose_name=_('Student'),
        to=Student,
        on_delete=models.SET_NULL,
        null=True,
        related_name='test_attempts',
    )
    test = models.ForeignKey(
        verbose_name=_('Attempted test'),
        to=SectionTest,
        on_delete=models.CASCADE,
        related_name='attempts',
    )
    answered_correctly = models.PositiveSmallIntegerField(
        verbose_name=_('Answered correctly'),
        default=0,
    )

    @property
    def score(self):
        return self.answered_correctly * self.test.score_per_question

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
        return self.test.is_open and self.attempts_left > 0

    class Meta:
        verbose_name = _('Student test attempt')
        verbose_name_plural = _('Student test attempts')
