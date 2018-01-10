from . import models

from django.contrib import admin

class TagAdmin(admin.ModelAdmin):
  list_display = ("name", "household", "id")
  list_filter = ()
  raw_id_fields = ("household",)
  search_fields = ("name",)
  ordering = ("name",)

admin.site.register(models.Tag, TagAdmin)
