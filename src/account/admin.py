from . import models

from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
  list_display = ("name", "household", "owner")
  list_filter = ()
  raw_id_fields = ("household", "owner")
  search_fields = ("name",)
  ordering = ("name",)

admin.site.register(models.Account, AccountAdmin)
