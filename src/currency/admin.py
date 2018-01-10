from . import models

from django.contrib import admin

class CurrencyAdmin(admin.ModelAdmin):
  list_display = ("iso_code", "symbol", "id")
  list_filter = ()
  raw_id_fields = ()
  search_fields = ("iso_code", "symbol")
  ordering = ("iso_code",)

admin.site.register(models.Currency, CurrencyAdmin)
