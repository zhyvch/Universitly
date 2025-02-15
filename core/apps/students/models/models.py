from core.apps.students.models import StudentManager
from core.apps.users.models import User

class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

