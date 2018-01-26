from geo.models import Language

from django.db import models

#class MailFragment(models.Model):
#  reference = models.CharField(max_length=128, unique=True)
#  body = models.TextField(blank=True, default="")
#  # TODO

class MailSignature(models.Model):
  language = models.OneToOneField(Language, on_delete=models.CASCADE)
  body = models.TextField(blank=True, default="")

  def __str__(self):
    return str(self.language)

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
