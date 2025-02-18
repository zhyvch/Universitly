from django.urls import path, include

urlpatterns = [
    path('education/', include('core.apps.education.urls')),
    path('users/', include('core.apps.users.urls')),
    path('students/', include('core.apps.students.urls')),
    path('teachers/', include('core.apps.teachers.urls')),
]