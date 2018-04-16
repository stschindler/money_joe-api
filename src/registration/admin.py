from . import models

from django.contrib import admin

class AccountActivationAdmin(admin.ModelAdmin):
  list_display = ("user", "creation_time", "activation_time", "code", "ip")
  list_filter = ("creation_time", "activation_time")
  raw_id_fields = ("user",)
  search_fields = ("user__email", "user__username")
  ordering = ("user",)

admin.site.register(models.AccountActivation, AccountActivationAdmin)
