
from django.urls import path
from .views import IceCreamIndexView, create_ice_cream

app_name = 'icecream'

urlpatterns = [
    path('create/icecream', create_ice_cream, name='create_icecream'),
    path('icecream', IceCreamIndexView.as_view(), name='icecream_index'),
]
