from django.db import models
from django.db.models import Q, F, Func
from django.db.models.constraints import CheckConstraint
from django.db.models.functions import Length
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.apps.common.models import TitledTimestampedBaseModel, TitledBaseModel
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

    @property
    def number_of_courses(self):
        return self.courses.count()

    @property
    def number_of_admins(self):
        return self.admins.count()

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

    @property
    def number_of_sections(self):
        return self.sections.count()

    @property
    def number_of_teachers(self):
        return self.teachers.count()

    @property
    def number_of_students(self):
        return self.students.count()

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

    @property
    def is_lecture(self):
        return self.type == self.SectionType.LECTURE

    @property
    def is_homework(self):
        return self.type == self.SectionType.HOMEWORK

    @property
    def is_test(self):
        return self.type == self.SectionType.TEST

    @property
    def number_of_files(self):
        return self.files.count()

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


class SectionHomework(TitledBaseModel):
    section = models.OneToOneField(
        verbose_name=_('Related section'),
        to=Section,
        on_delete=models.CASCADE,
        related_name='homework',
    )
    content = models.TextField(
        verbose_name=_('Content'),
        blank=True,
    )
    deadline = models.DateTimeField(
        verbose_name=_('Deadline'),
        blank=True,
    )

    @property
    def all_students_submitted(self):
        return self.homeworks.count() == self.section.course.students.count()

    class Meta:
        verbose_name = _('Section homework')
        verbose_name_plural = _('Section homeworks')
        constraints = [
            CheckConstraint(
                condition=Q(deadline__gt=timezone.now()),
                name='deadline_gt_now',
            ),
        ]

    def __str__(self):
        return self.title


class SectionTest(TitledBaseModel):
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
    start_date = models.DateTimeField(
        verbose_name=_('Start date'),
        default=timezone.now,
    )
    end_date = models.DateTimeField(
        verbose_name=_('End date'),
    )

    @property
    def is_open(self):
        return self.start_date <= timezone.now() < self.end_date

    @property
    def questions_count(self):
        return Length(Func(F('questions'), function='jsonb_object_keys'))

    @property
    def score_per_question(self):
        return F('max_points') / self.questions_count

    @property
    def number_of_attempts(self):
        return self.attempts.count()

    def letter_grades_to_score_bound(self):
        return {
            'A': self.max_score * 0.9,
            'B': self.max_score * 0.8,
            'C': self.max_score * 0.7,
            'D': self.max_score * 0.6,
            'F': 0,
        }

    def get_letter_grade(self, score):
        for grade, score_bound in self.letter_grades_to_score_bound().items():
            if score >= score_bound:
                return grade

    class Meta:
        verbose_name = _('Section test')
        verbose_name_plural = _('Section tests')
        constraints = [
            CheckConstraint(
                condition=Q(max_score__gte=F('passing_score')),
                name='max_score_gte_passing_score',
            ),
            models.CheckConstraint(
                condition=Q(start_date__gte=timezone.now()),
                name='start_date_gte_now',
            ),
            models.CheckConstraint(
                condition=Q(end_date__gt=F('start_date')),
                name='end_date_gt_start_date',
            ),
        ]

    def __str__(self):
        return self.title
