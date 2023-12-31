from django.db import models
from accounts.models import CustomUser 
from django.utils.safestring import mark_safe
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class DiaryTable(models.Model):
  user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
  date = models.DateField()
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

