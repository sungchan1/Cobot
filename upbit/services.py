import os

import requests
from dotenv import load_dotenv
import pyupbit

from upbit.models import AccountInfo

# from .models import AccountInfo

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
API_KEY = os.getenv("UPBIT_OPEN_API_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_OPEN_API_SECRET_KEY")

# PyUpbit 객체 생성
upbit = pyupbit.Upbit(API_KEY, SECRET_KEY)

# 내 계좌 정보 가져오기
def get_account_info():
    data = upbit.get_balances()

    # 현재가 API 호출
    coin_symbols = [item['currency'] for item in data if item['currency'] != 'KRW']
    market_query = ','.join([f'KRW-{symbol}' for symbol in coin_symbols])
    url = f"https://api.upbit.com/v1/ticker?markets={market_query}"
    response = requests.get(url)
    ticker_data = response.json()

    # 현재가 매핑
    prices = {item['market'].split('-')[1]: item['trade_price'] for item in ticker_data}

    # 총 가치 계산 추가
    for item in data:
        currency = item['currency']
        balance = float(item['balance'])
        if currency == 'KRW':
            item['total_price'] = balance
        else:
            current_price = prices.get(currency, 0)
            item['total_price'] = balance * current_price



    print(data)
    return data


def save_account_info(data):
    """
    계좌 정보를 데이터베이스에 저장합니다.
    :param data: JSON 형태의 계좌 정보 리스트
    """
    for account in data:
        AccountInfo.objects.update_or_create(
            currency=account['currency'],
            defaults={
                'balance': account['balance'],
                'locked': account['locked'],
                'avg_buy_price': account['avg_buy_price'],
                'avg_buy_price_modified': account['avg_buy_price_modified'],
                'unit_currency': account['unit_currency'],
            }
        )


