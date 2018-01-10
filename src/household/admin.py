from . import models

from django.contrib import admin

class HouseholdAdmin(admin.ModelAdmin):
  list_display = ("name", "id")
  list_filter = ()
  raw_id_fields = ()
  search_fields = ("name",)
  ordering = ("name",)

class HouseholdMembershipAdmin(admin.ModelAdmin):
  list_display = ("household", "user", "level", "id")
  list_filter = ("level",)
  raw_id_fields = ("household", "user")
  search_fields = ("household__name", "user__username")
  ordering = ("household", "user")

admin.site.register(models.Household, HouseholdAdmin)
admin.site.register(models.HouseholdMembership, HouseholdMembershipAdmin)
