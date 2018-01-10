from . import models

from django.contrib import admin

class JournalEntryTagInline(admin.TabularInline):
  model = models.JournalEntryTag
  extra = 0

class JournalEntryAdmin(admin.ModelAdmin):
  list_display = (
    "description", "creation_time", "booking_time", "valuta_time",
    "household", "creator", "id"
  )
  list_filter = ("creation_time", "booking_time", "valuta_time")
  raw_id_fields = ("creator",)
  search_fields = ("description",)
  ordering = ("creation_time",)
  inlines = (JournalEntryTagInline,)

admin.site.register(models.JournalEntry, JournalEntryAdmin)
