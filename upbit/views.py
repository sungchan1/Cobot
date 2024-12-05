from django.shortcuts import render
from .models import AccountInfo
from django.core.serializers.json import DjangoJSONEncoder
import json

from .services import get_account_info


def account_info_view(request):
    # 모든 AccountInfo 데이터 가져오기
    account_data = get_account_info()

    # Chart.js용 데이터 준비
    chart_data = {
        'labels': [item['currency'] for item in account_data],
        'values': [item['total_price'] for item in account_data],
    }

    # 모든 자산의 총합 계산
    total_assets_value = sum(item['total_price'] for item in account_data)

    return render(request, 'upbit/account_info.html', {
        'account_info': account_data,
        'chart_data': json.dumps(chart_data),  # JSON으로 변환
        'total_assets_value': total_assets_value,  # 총합 전달
    })


def account_chart_view(request):
    # QuerySet 가져오기
    accounts = get_account_info()

    # 데이터를 JSON 형식으로 변환
    account_chart_data = [
        {
            "currency": account.currency,
            "balance": float(account.balance)
        }
        for account in accounts
    ]
    # JSON 데이터를 문자열로 직렬화
    context = {
        "account_chart_info": json.dumps(account_chart_data, cls=DjangoJSONEncoder)
    }
    return render(request, 'upbit/account_info_chart.html', context)