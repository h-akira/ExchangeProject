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

class EventTable(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  title = models.CharField(max_length=127)
  dt = models.DateTimeField()
  country = models.CharField(max_length=31, choices=COUNTRY)
  description = models.TextField()

class DiaryTable(models.Model):
  user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
  date = models.DateField(unique=True)
  text = models.TextField(null=True, blank=True)
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user", "date"],
        name="date_unique"
      )
    ]
