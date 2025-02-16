from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.apps.common.models import TitledTimestampedBaseModel
from core.config.settings import AUTH_USER_MODEL


class Institution(TitledTimestampedBaseModel):
    class InstitutionType(models.TextChoices):
        SCHOOL = 'SCHOOL', _('School')
        UNIVERSITY = 'UNI', _('University')
        OTHER = 'OTHER', _('Other')

    type = models.CharField(
        verbose_name=_('Type'),
        choices=InstitutionType,
        default=InstitutionType.OTHER,
    )
    icon = models.ImageField(
        verbose_name=_('Icon'),
        upload_to='institutions/',
    )
    owner = models.ForeignKey(
        verbose_name=_('Owner'),
        to=AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='owned_institutions',
        null=True,
    )
    admins = models.ManyToManyField(
        verbose_name=_('Admins'),
        to=AUTH_USER_MODEL,
        related_name='administrated_institutions',
    )

    class Meta:
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')

    def __str__(self):
        return self.title


class Course(TitledTimestampedBaseModel):
    institution = models.ForeignKey(
        verbose_name=_('Related institution'),
        to=Institution,
        on_delete=models.CASCADE,
        related_name='courses',
    )
    teachers = models.ManyToManyField(
        verbose_name=_('Teachers'),
        to=AUTH_USER_MODEL,
        related_name='teaching_courses',
    )
    students = models.ManyToManyField(
        verbose_name=_('Students'),
        to=AUTH_USER_MODEL,
        related_name='enrolled_courses',
    )

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __str__(self):
        return self.title



class Section(TitledTimestampedBaseModel):
    class SectionType(models.TextChoices):
        LECTURE = 'L', _('Lecture')
        HOMEWORK = 'HW', _('Homework')
        TEST = 'T', _('Test')

    course = models.ForeignKey(
        verbose_name=_('Related course'),
        to=Course,
        on_delete=models.CASCADE,
        related_name='sections',
    )
    type = models.CharField(
        verbose_name=_('Type'),
        choices=SectionType,
        default=SectionType.LECTURE,
    )
    content = models.TextField(
        verbose_name=_('Content'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Section')
        verbose_name_plural = _('Sections')

    def __str__(self):
        return self.title


class SectionFile(models.Model):
    section = models.ForeignKey(
        verbose_name=_('Related section'),
        to=Section,
        on_delete=models.CASCADE,
        related_name='files',
    )
    file = models.FileField(
        verbose_name=_('File'),
        upload_to='section_files/',
    )

    class Meta:
        verbose_name = _('Section file')
        verbose_name_plural = _('Section files')

    def __str__(self):
        return self.file.name


class SectionTest(TitledTimestampedBaseModel):
    section = models.OneToOneField(
        verbose_name=_('Related section'),
        to=Section,
        on_delete=models.CASCADE,
        related_name='test',
    )
    questions = models.JSONField(
        verbose_name=_('Questions'),
    )
    max_score = models.PositiveIntegerField(
        verbose_name=_('Max score'),
        default=100,
    )
    passing_score = models.PositiveIntegerField(
        verbose_name=_('Passing score'),
        default=50,
    )
    max_attempts = models.PositiveIntegerField(
        verbose_name=_('Attempts'),
        default=1,
    )
    deadline = models.DateTimeField(
        verbose_name=_('Deadline'),
    )

    @property
    def is_open(self):
        return self.deadline > timezone.now()

    def letter_grades_to_score_bound(self):
        return {
            'A': self.max_score * 0.9,
            'B': self.max_score * 0.8,
            'C': self.max_score * 0.7,
            'D': self.max_score * 0.6,
            'F': self.max_score * 0.5,
        }

    def get_letter_grade(self, score):
        for grade, score_bound in self.letter_grades_to_score_bound().items():
            if score >= score_bound:
                return grade

    class Meta:
        verbose_name = _('Section test')
        verbose_name_plural = _('Section tests')

    def __str__(self):
        return self.title
