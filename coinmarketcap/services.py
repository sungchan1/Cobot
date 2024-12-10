from django.core.cache import cache
import requests
import os
from dotenv import load_dotenv

from coinmarketcap.models import Quote, CoinTag, Tag, Coin

# .env 파일 로드
load_dotenv()

# CoinMarketCap API 키
API_KEY = os.getenv("COINMARKETCAP_API_KEY")


def fetch_coin_data(limit=50):
    """
    CoinMarketCap API에서 코인 데이터를 가져옵니다.
    데이터를 캐시하여 10분 동안 유지합니다.
    """
    # 캐시 키
    cache_key = f"coin_data_{limit}"
    # 캐시에서 데이터 가져오기
    cached_data = cache.get(cache_key)

    if cached_data:
        print("캐시에서 데이터 반환")
        return cached_data

    # 캐시에 데이터가 없으면 API 호출
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }
    params = {
        "start": "1",        # 시작 순위
        "limit": limit,      # 가져올 코인 수
        "sort": "market_cap",# 정렬 기준: 시가총액
        "convert": "USD",    # 가격 변환 통화
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json().get('data', [])
        # API 데이터를 캐시에 저장 (10분 동안 유지)
        cache.set(cache_key, data, timeout=600)
        return data
    except requests.exceptions.RequestException as e:
        print(f"데이터 가져오기 오류: {e}")
        return []


def get_top_20_non_stable_coins():
    """
    스테이블 코인을 제외한 상위 20개 코인을 반환합니다.
    :return: 스테이블 코인을 제외한 상위 20개 코인 리스트
    """
    coin_data = fetch_coin_data(limit=50)  # 스테이블 코인을 제외하기 위해 더 많이 가져옴
    filtered_coins = [coin for coin in coin_data if "stablecoin" not in coin.get('tags', [])]

    top_20_coins = filtered_coins[:20]
    save_coin_data(top_20_coins)
    return top_20_coins




def save_coin_data(data):
    """
    CoinMarketCap API 데이터를 DB에 저장.
    """
    for coin_data in data:
        # Coin 저장
        coin, created = Coin.objects.update_or_create(
            id=coin_data["id"],
            defaults={
                "name": coin_data["name"],
                "symbol": coin_data["symbol"],
                "slug": coin_data["slug"],
                "num_market_pairs": coin_data["num_market_pairs"],
                "date_added": coin_data["date_added"],
                "max_supply": coin_data.get("max_supply"),
                "circulating_supply": coin_data["circulating_supply"],
                "total_supply": coin_data["total_supply"],
                "infinite_supply": coin_data["infinite_supply"],
                "cmc_rank": coin_data["cmc_rank"],
                "last_updated": coin_data["last_updated"],
            },
        )

        # Tag 저장
        for tag_name in coin_data.get("tags", []):
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            CoinTag.objects.get_or_create(coin=coin, tag=tag)

        # Quote 저장
        usd_quote = coin_data["quote"]["USD"]
        Quote.objects.update_or_create(
            coin=coin,
            defaults={
                "price": usd_quote["price"],
                "volume_24h": usd_quote["volume_24h"],
                "volume_change_24h": usd_quote.get("volume_change_24h"),
                "percent_change_1h": usd_quote.get("percent_change_1h"),
                "percent_change_24h": usd_quote.get("percent_change_24h"),
                "percent_change_7d": usd_quote.get("percent_change_7d"),
                "percent_change_30d": usd_quote.get("percent_change_30d"),
                "percent_change_60d": usd_quote.get("percent_change_60d"),
                "percent_change_90d": usd_quote.get("percent_change_90d"),
                "market_cap": usd_quote["market_cap"],
                "market_cap_dominance": usd_quote.get("market_cap_dominance"),
                "fully_diluted_market_cap": usd_quote.get("fully_diluted_market_cap"),
                "last_updated": usd_quote["last_updated"],
            },
        )
