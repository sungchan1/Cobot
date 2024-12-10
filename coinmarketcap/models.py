from django.db import models

# Create your models here.
from django.db import models

class Coin(models.Model):
    id = models.IntegerField(primary_key=True)  # CoinMarketCap ID
    name = models.CharField(max_length=100)  # 코인 이름
    symbol = models.CharField(max_length=10)  # 코인 심볼
    slug = models.CharField(max_length=100)  # URL-friendly 이름
    num_market_pairs = models.IntegerField()  # 마켓 페어 개수
    date_added = models.DateTimeField()  # 코인 등록일
    max_supply = models.BigIntegerField(null=True, blank=True)  # 최대 공급량
    circulating_supply = models.FloatField()  # 유통 공급량
    total_supply = models.FloatField()  # 총 공급량
    infinite_supply = models.BooleanField(default=False)  # 무한 공급 여부
    cmc_rank = models.IntegerField()  # 시가총액 순위
    last_updated = models.DateTimeField()  # 마지막 업데이트 시간

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 태그 이름

    def __str__(self):
        return self.name


class CoinTag(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name="tags")  # Coin과 관계
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # Tag와 관계

    class Meta:
        unique_together = ("coin", "tag")  # 중복 방지


class Quote(models.Model):
    coin = models.OneToOneField(Coin, on_delete=models.CASCADE, related_name="quote")  # Coin과 1:1 관계
    price = models.FloatField()  # 현재 가격
    volume_24h = models.FloatField()  # 24시간 거래량
    volume_change_24h = models.FloatField(null=True, blank=True)  # 24시간 거래량 변화율
    percent_change_1h = models.FloatField(null=True, blank=True)  # 1시간 가격 변화율
    percent_change_24h = models.FloatField(null=True, blank=True)  # 24시간 가격 변화율
    percent_change_7d = models.FloatField(null=True, blank=True)  # 7일 가격 변화율
    percent_change_30d = models.FloatField(null=True, blank=True)  # 30일 가격 변화율
    percent_change_60d = models.FloatField(null=True, blank=True)  # 60일 가격 변화율
    percent_change_90d = models.FloatField(null=True, blank=True)  # 90일 가격 변화율
    market_cap = models.FloatField()  # 시가총액
    market_cap_dominance = models.FloatField(null=True, blank=True)  # 시가총액 점유율
    fully_diluted_market_cap = models.FloatField(null=True, blank=True)  # 완전 희석 시가총액
    last_updated = models.DateTimeField()  # 마지막 업데이트 시간

    def __str__(self):
        return f"Quote for {self.coin.name}"