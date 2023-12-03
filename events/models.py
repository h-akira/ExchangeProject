from django.db import models
from api.models import EventTable
from accounts.models import CustomUser
from django.utils.safestring import mark_safe
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class EventCommentTable(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  event = models.ForeignKey(EventTable, on_delete=models.CASCADE)
  text = MarkdownxField(null=True, blank=True)
  def get_text_markdownx(self):
    return mark_safe(markdownify(self.text))
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=["user", "event"],
        name="user_event_unique"
      )
    ]
