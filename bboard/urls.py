from django.urls import path, re_path
from .views import (BbIndexView, BbByRubricView, BbCreateView, RubricCreateView, BbDetailView, BbEditView, BbDeleteView,
                    BbRedirectView, BbMonthView, AllUsersView, UserDetailView, RecordView, PostListView)

# BbMonthView BbPostView
app_name = 'bboard'

urlpatterns = [
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('add/rubric/', RubricCreateView.as_view(), name='add_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('update/<int:pk>/', BbEditView.as_view(), name='update'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    # path('', index, name='index'),
    path('', BbIndexView.as_view(), name='index'),
    path('year/<int:year>/', BbRedirectView.as_view(), name='redirect'),
    path('<int:year>/<int:month>/', BbMonthView.as_view(), name='month'),
    path('all_users/', AllUsersView.as_view(), name='all_users'),
    path('user_details/', UserDetailView.as_view(), name='user_details'),
    path('record_list/', RecordView.as_view(), name='record_list'),
    path('post_list/', PostListView.as_view(), name='post_list'),
]
