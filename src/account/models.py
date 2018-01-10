from household.models import Household

from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models

class Account(models.Model):
  class Meta:
    unique_together = (("household", "reference"),)

  household = models.ForeignKey(
    Household, related_name="accounts", on_delete=models.CASCADE
  )
  reference = models.CharField(max_length=128)
  name = models.CharField(max_length=128, blank=True, default="")
  owner = models.ForeignKey(
    User, related_name="owned_accounts", on_delete=models.CASCADE
  )
  meta = JSONField(default=dict, blank=True)

  def __str__(self):
    return self.reference
