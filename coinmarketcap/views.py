from django.http import JsonResponse
from django.shortcuts import render

from .services import get_top_20_non_stable_coins

def top_20_coins_view(request):
    """
    상위 20개 비스테이블 코인을 JSON으로 반환합니다.
    """
    top_coins = get_top_20_non_stable_coins()
    return JsonResponse({'top_20_coins': top_coins})


def top_20_coins_table_view(request):
    """
    상위 20개 비스테이블 코인을 테이블 형식으로 렌더링합니다.
    """
    top_coins = get_top_20_non_stable_coins()
    return render(request, 'coinmarketcap/top_20_coins.html', {'top_coins': top_coins})