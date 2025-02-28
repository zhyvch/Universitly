from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from core.config.settings.debug_toolbar.setup import DebugToolbarSetup

urlpatterns = DebugToolbarSetup.do_urls(urlpatterns)
