from django.db import models

class Country(models.Model):
  class Meta:
    verbose_name_plural = "Countries"

  iso_code = models.CharField(max_length=4, unique=True)
  name = models.CharField(max_length=64)

  def __str__(self):
    return self.iso_code

class Language(models.Model):
  locale_name = models.CharField(max_length=8, unique=True)
  name = models.CharField(max_length=128)
  country = models.ForeignKey(
    Country, related_name="languages", on_delete=models.CASCADE
  )

  def __str__(self):
    return self.locale_name
