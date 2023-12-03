from django.db import models
from accounts.models import CustomUser 

COUNTRY = (
  ("USA","アメリカ"),
  ("EU", "EU"),
  ("Japan","日本"),
  ("Germany","ドイツ"),
  ("UK","イギリス"),
  ("France","フランス"),
  ("Canada","カナダ"),
  ("Australia","オーストラリア"),
  ("NewZealand","ニュージーランド"),
  ("Swiss","スイス"),
  ("Turkey","トルコ"),
  ("China","中国"),
  ("Mexico","メキシコ"),
  ("Other","その他"),
)

dic_full = {
  "Japan": "日本",
  "EU": "EU",
  "USA": "アメリカ",
  "Germany": "ドイツ",
  "UK": "イギリス",
  "France": "フランス",
  "Canada": "カナダ",
  "Australia": "オーストラリア",
  "NewZealand": "ニュージーランド",
  "Swiss": "スイス",
  "Turkey": "トルコ",
  "China": "中国",
  "Mexico": "メキシコ",
  "Other": "その他"
}

dic_omit = {
  "Japan": "日",
  "EU": "欧",
  "USA": "米",
  "Germany": "独",
  "UK": "英",
  "France": "仏",
  "Canada": "加",
  "Australia": "豪",
  "NewZealand": "新",
  "Swiss": "瑞",
  "Turkey": "土",
  "China": "中",
  "Mexico": "墨",
  "Other": "他"
}

class ExchangeDataTable(models.Model):
  dt = models.DateTimeField()
  pair = models.CharField(max_length=15)  # USDJPYなど（/なし）
  Open = models.FloatField()
  High = models.FloatField()
  Low = models.FloatField()
  Close = models.FloatField()
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["dt", "pair"],
        name="time_unique"
      )
    ]

class EventTable(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=127)
  date = models.DateField()
  time = models.TimeField(null=True, blank=True)
  country = models.CharField(max_length=31, choices=COUNTRY)
  importance = models.IntegerField(null=True, blank=True)
  previous = models.CharField(max_length=63, null=True, blank=True)
  prediction = models.CharField(max_length=63, null=True, blank=True)
  result = models.CharField(max_length=63, null=True, blank=True)
  influence = models.CharField(max_length=63, null=True, blank=True)
  def country_jp_full(self):
    return dic_full[self.country]
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user", "name", "date", "time", "country"],
        name="event_unique"
      )
    ]
