from . import models

from django.contrib import admin

class AuthTokenAdmin(admin.ModelAdmin):
  list_display = ("token", "user", "creation_time", "last_use_time")
  list_filter = ("creation_time", "last_use_time")
  raw_id_fields = ("user",)
  search_fields = ("token",)
  ordering = ("creation_time",)

admin.site.register(models.AuthToken, AuthTokenAdmin)
