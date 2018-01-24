from . import models

from django.contrib import admin

class CountryAdmin(admin.ModelAdmin):
  list_display = ("iso_code", "name")
  list_filter = ()
  raw_id_fields = ()
  search_fields = ("iso_code", "name")
  ordering = ("iso_code",)

class LanguageAdmin(admin.ModelAdmin):
  list_display = ("locale_name", "name", "country")
  list_filter = ("country",)
  raw_id_fields = ("country",)
  search_fields = ("locale_name", "name", "country__name")
  ordering = ("locale_name",)

admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.Language, LanguageAdmin)
