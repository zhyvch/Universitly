from rest_framework.viewsets import ViewSet

from core.apps.education.apis import (
    InstitutionCreateAPI, InstitutionListAPI, InstitutionUpdateAPI, InstitutionDeleteAPI
)

from rest_framework.routers import SimpleRouter

class InstitutionViewSet(ViewSet):
    def list(self, request):
        return InstitutionListAPI.as_view()(request._request)

    def create(self, request):
        return InstitutionCreateAPI.as_view()(request._request)

    def partial_update(self, request, pk=None):
        return InstitutionUpdateAPI.as_view()(request._request, institution_id=pk)

    def destroy(self, request, pk=None):
        return InstitutionDeleteAPI.as_view()(request._request, institution_id=pk)

router = SimpleRouter()
router.register('institutions', InstitutionViewSet, basename='institution')

urlpatterns = router.urls
