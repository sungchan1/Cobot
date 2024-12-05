from django.db import models

# Create your models here.

class AccountInfo(models.Model):
    """
    계좌 정보를 저장하는 모델
    """
    currency = models.CharField(max_length=10)  # 코인의 심볼 (예: BTC, ETH)
    balance = models.DecimalField(max_digits=20, decimal_places=10)  # 잔액
    locked = models.DecimalField(max_digits=20, decimal_places=10)  # 잠금된 금액
    avg_buy_price = models.DecimalField(max_digits=20, decimal_places=10)  # 평균 매수가격
    avg_buy_price_modified = models.BooleanField()  # 평균 매수가격 수정 여부
    unit_currency = models.CharField(max_length=10)  # 기준 화폐 (예: KRW)

    def __str__(self):
        return f"{self.currency}: {self.balance} {self.unit_currency}"
