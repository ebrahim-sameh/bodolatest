from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # standard django admin panel
    path("admin/", admin.site.urls),
    # our referral system endpoints
    path("api/v1/", include("referral_system.urls")),
    path("api/v1/", include("tasks.urls")),
    path("api/v1/", include("user.urls")),
    # djoser 
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("auth/", include("djoser.urls.jwt")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)