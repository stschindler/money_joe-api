from django.db import models

class Currency(models.Model):
  iso_code = models.CharField(max_length=3, unique=True)
  symbol = models.CharField(max_length=4)

  def __str__(self):
    return self.iso_code
