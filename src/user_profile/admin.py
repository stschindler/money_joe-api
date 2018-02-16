from . import models

from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ("user", "language")
  list_filter = ("language",)
  raw_id_fields = ("user",)
  search_fields = ("user__username",)
  ordering = ("user__username",)

admin.site.register(models.UserProfile, UserProfileAdmin)
