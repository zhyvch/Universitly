from rest_framework.viewsets import ViewSet
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter

from core.apps.education.apis import (
    InstitutionCreateAPI, InstitutionListAPI, InstitutionUpdateAPI, InstitutionDeleteAPI,
    CourseCreateAPI, CourseListAPI, #CourseUpdateAPI, CourseDeleteAPI
)


class InstitutionViewSet(ViewSet):
    def create(self, request):
        return InstitutionCreateAPI.as_view()(request._request)

    def list(self, request):
        return InstitutionListAPI.as_view()(request._request)

    def partial_update(self, request, pk=None):
        return InstitutionUpdateAPI.as_view()(request._request, institution_id=pk)

    def destroy(self, request, pk=None):
        return InstitutionDeleteAPI.as_view()(request._request, institution_id=pk)


class CourseViewSet(ViewSet):
    def create(self, request, institution_pk=None):
        return CourseCreateAPI.as_view()(request._request, institution_id=institution_pk)

    def list(self, request, institution_pk=None):
        return CourseListAPI.as_view()(request._request, institution_id=institution_pk)

    # def partial_update(self, request, pk=None, institution_id=None):
    #     return CourseUpdateAPI.as_view()(request._request, institution_id=institution_id, course_id=pk)
    #
    # def destroy(self, request, pk=None, institution_id=None):
    #     return CourseDeleteAPI.as_view()(request._request, institution_id=institution_id, course_id=pk)


institutions_router = SimpleRouter()
institutions_router.register(r'institutions', InstitutionViewSet, basename='institution')

courses_router = NestedSimpleRouter(institutions_router, r'institutions', lookup='institution')
courses_router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = institutions_router.urls + courses_router.urls
