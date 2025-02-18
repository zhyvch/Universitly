from django.db import models


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True)

    def create(self, **kwargs):
        kwargs['is_teacher'] = True
        return super().create(**kwargs)
