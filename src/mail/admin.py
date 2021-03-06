from . import models

from django.contrib import admin

class MailFragmentAdmin(admin.ModelAdmin):
  list_display = ("reference", "language", "body")
  list_filter = ("language",)
  raw_id_fields = ("language",)
  search_fields = ("reference", "body")
  ordering = ("reference",)

class MailTemplateAdmin(admin.ModelAdmin):
  list_display = ("reference", "language", "subject", "signature_included")
  list_filter = ("reference", "language", "signature_included")
  raw_id_fields = ("language",)
  search_fields = ("reference", "subject", "body")
  ordering = ("reference", "language")

class MailSignatureAdmin(admin.ModelAdmin):
  list_display = ("language", "body")
  list_filter = ("language",)
  raw_id_fields = ("language",)
  search_fields = ("body",)
  ordering = ("language",)

admin.site.register(models.MailFragment, MailFragmentAdmin)
admin.site.register(models.MailSignature, MailSignatureAdmin)
admin.site.register(models.MailTemplate, MailTemplateAdmin)
