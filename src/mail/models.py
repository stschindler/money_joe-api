from geo.models import Language

from django.db import models

class MailSignature(models.Model):
  language = models.ForeignKey(
    Language, related_name="mail_signatures", on_delete=models.CASCADE,
    unique=True,
  )
  body = models.TextField(blank=True, default="")

class MailTemplate(models.Model):
  class Meta:
    unique_together = (("reference", "language"),)

  reference = models.CharField(max_length=64)
  language = models.ForeignKey(
    Language, related_name="mail_templates", on_delete=models.CASCADE
  )
  subject = models.CharField(max_length=256, default="")
  body = models.TextField(blank=True, default="")
  signature_included = models.BooleanField(default=True)

  def __str__(self):
    return "{} {}".format(self.handle, self.language)
