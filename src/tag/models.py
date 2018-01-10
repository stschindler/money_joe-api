from household.models import Household

from django.db import models

class Tag(models.Model):
  name = models.CharField(max_length=128)
  household = \
    models.ForeignKey(Household, related_name="tags", on_delete=models.CASCADE)

  def __str__(self):
    return self.name

