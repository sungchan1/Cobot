from django.urls import path
from .views import account_info_view, account_chart_view

urlpatterns = [
    path('account/', account_info_view, name='account_info'),
]