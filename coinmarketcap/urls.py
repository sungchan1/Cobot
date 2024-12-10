from django.urls import path
from .views import top_20_coins_view, top_20_coins_table_view

urlpatterns = [
    path('top-20-coins/', top_20_coins_view, name='top_20_coins'),
    path('top-20-coins-table/', top_20_coins_table_view, name='top_20_coins_table'),


]
