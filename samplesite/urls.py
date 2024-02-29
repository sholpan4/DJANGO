from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', include('testapp.urls', namespace='test')),
    path('', include('bboard.urls', namespace='bboard')),
]

urlpatterns += [
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings) # DEBUG = True
