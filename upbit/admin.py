from django.contrib import admin
from upbit.models import AccountInfo


# Register your models here.
@admin.register(AccountInfo)
class AccountInfoAdmin(admin.ModelAdmin):
    list_display = ('currency', 'balance', 'locked', 'avg_buy_price', 'unit_currency')
    search_fields = ('currency', 'unit_currency')
