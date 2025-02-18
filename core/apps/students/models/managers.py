from django.db import models


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_student=True)

    def create(self, **kwargs):
        kwargs['is_student'] = True
        return super().create(**kwargs)
