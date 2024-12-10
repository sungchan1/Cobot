from django.urls import path
from .views import *


app_name = 'upbit'

urlpatterns = [
    path('account/', account_info_view, name='account'),
    path('', service_list, name='service_list'),

]