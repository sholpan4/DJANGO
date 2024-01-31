from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', include('testapp.urls', namespace='test')),
    path('todolist', include('todolist.urls', namespace='todolist')),
    path('', include('bboard.urls', namespace='bboard')),
]
