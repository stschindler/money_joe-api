from . import models

from django.contrib import admin

class CurrencyAdmin(admin.ModelAdmin):
  list_display = ("iso_code", "symbol", "id")
  list_filter = ()
  raw_id_fields = ()
  search_fields = ("iso_code", "symbol")
  ordering = ("iso_code",)

class CountryCurrencyAdmin(admin.ModelAdmin):
  list_display = ("country", "currency")
  list_filter = ("country", "currency")
  raw_id_fields = ()
  search_fields = ("country__name", "country__iso_code", "currency__iso_code")
  ordering = ("country__name", "currency__iso_code")

admin.site.register(models.CountryCurrency, CountryCurrencyAdmin)
admin.site.register(models.Currency, CurrencyAdmin)
