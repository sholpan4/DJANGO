"""
URL configuration for samplesite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from .views import (index, BbByRubricView, BbCreateView, RubricCreateView)

# from .views import (index, by_rubric, BbCreateView, add_and_save)
# add, add_save, details

app_name = 'bboard'

urlpatterns = [
    # path('add/', add_and_save, name='add'),
    path('add/rubric/', RubricCreateView.as_view(), name='add_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),

    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('', index, name='index'),
]

    # path('add/', BbCreateView.as_view(), name='add'),

    # path('add/save/', add_save, name='add_save'),
    # path('add/', add, name='add'),
    # path('detail/<int:bb_id>/', detail, name='bb_detail'),


    # re_path(r'^add/$', BbCreateView.as_view(), name='add'),
    # re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, name='by_rubric'),
    # re_path(r'^$', index, name='index'),
