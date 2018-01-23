from . import models

from django.contrib import admin

class AccountActivationAdmin(admin.ModelAdmin):
  list_display = ("user", "code", "creation_time", "activation_time", "ip")
  list_filter = ("creation_time", "activation_time")
  raw_id_fields = ("user",)
  search_fields = ("user__email", "user__username", "code")
  ordering = ("user",)

admin.site.register(models.AccountActivation, AccountActivationAdmin)
