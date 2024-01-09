from django.urls import path, re_path
from .views import (index, BbByRubricView, BbCreateView, RubricCreateView, BbDetailView)

# from .views import (index, by_rubric, BbCreateView, add_and_save)
# add, add_save, details

app_name = 'bboard'

urlpatterns = [
    # path('add/', add_and_save, name='add'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
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
