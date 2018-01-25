from geo.models import Country

from django.db import models

class Currency(models.Model):
  class Meta:
    verbose_name_plural = "Currencies"

  iso_code = models.CharField(max_length=3, unique=True)
  symbol = models.CharField(max_length=4)

  def __str__(self):
    return self.iso_code

class CountryCurrency(models.Model):
  class Meta:
    verbose_name_plural = "Country currencies"

  currency = models.ForeignKey(
    Currency, related_name="country_currencies", on_delete=models.CASCADE
  )
  country = models.ForeignKey(
    Country, related_name="country_currencies", on_delete=models.CASCADE
  )

  def __str__(self):
    return "{} {}".format(self.country, self.currency)
