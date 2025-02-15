from core.apps.teachers.models import TeacherManager
from core.apps.users.models import User

class Teacher(User):
    objects = TeacherManager()

    class Meta:
        proxy = True

