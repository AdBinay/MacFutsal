from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

SIGNATURE = getattr(settings,"SIGNATURE")

admin.site.site_header = SIGNATURE
admin.site.site_title = SIGNATURE + " Admin Portal"
admin.site.index_title = "Welcome to "+ SIGNATURE +" Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include("futsal.urls")),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('users.urls')),
]

# Handelling Static File while Development
if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)