from django.db import models
from accounts.models import CustomUser 
from django.utils.safestring import mark_safe
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

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
  name = models.CharField(max_length=127)
  date = models.DateField()
  time = models.TimeField(null=True, blank=True)
  country = models.CharField(max_length=31, choices=COUNTRY)
  importance = models.IntegerField(null=True, blank=True)
  previous = models.CharField(max_length=63, null=True, blank=True)
  prediction = models.CharField(max_length=63, null=True, blank=True)
  result = models.CharField(max_length=63, null=True, blank=True)
  description = models.TextField(null=True, blank=True)
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user", "name", "date", "time", "country"],
        name="event_unique"
      )
    ]

class DiaryTable(models.Model):
  user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
  date = models.DateField(unique=True)
  text = MarkdownxField(null=True, blank=True)
  def get_text_markdownx(self):
    return mark_safe(markdownify(self.text))
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user", "date"],
        name="date_unique"
      )
    ]
  def __str__(self):
    return self.date.strftime("%Y-%m-%d")+f"({self.user.username})"

