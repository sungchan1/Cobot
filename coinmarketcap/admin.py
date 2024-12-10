from django.contrib import admin
from .models import Coin, Tag, CoinTag, Quote


# Register your models here.
@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "symbol", "cmc_rank", "last_updated")
    search_fields = ("name", "symbol")
    list_filter = ("cmc_rank",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("coin", "price", "market_cap", "last_updated")
