from django.urls import path

from core.apps.education.apis import (
    InstitutionCreateAPI, InstitutionListAPI, InstitutionUpdateAPI, InstitutionDeleteAPI
)

urlpatterns = [
    path('institutions/create/', InstitutionCreateAPI.as_view(), name='create_institution'),
    path('institutions/', InstitutionListAPI.as_view(), name='institutions'),
    # path('institutions/<int:institution_id>/', InstitutionDetailAPI.as_view(), name='institution'),
    path('institutions/<int:institution_id>/update/', InstitutionUpdateAPI.as_view(), name='update_institution'),
    path('institutions/<int:institution_id>/delete/', InstitutionDeleteAPI.as_view(), name='delete_institution'),
]