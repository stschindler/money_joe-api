from account.models import Account
from household.models import Household
from tag.models import Tag

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class JournalEntry(models.Model):
  description = models.TextField(blank=True, default="")
  creation_time = models.DateTimeField()
  booking_time = models.DateTimeField()
  valuta_time = models.DateTimeField()
  creator = models.ForeignKey(
    User, related_name="created_journal_entries", on_delete=models.CASCADE
  )
  household = models.ForeignKey(
    Household, related_name="journal_entries", on_delete=models.CASCADE
  )
  debit_account = models.ForeignKey(
    Account, related_name="debit_journal_entries", on_delete=models.CASCADE,
    blank=True, null=True, default=None
  )
  credit_account = models.ForeignKey(
    Account, related_name="credit_journal_entries", on_delete=models.CASCADE,
    blank=True, null=True, default=None
  )

  def __str__(self):
    return str(self.description)

  def save(self, *args, **kwargs):
    if self.id is None and self.creation_time is None:
      self.creation_time = timezone.now()

    return super().save(*args, **kwargs)

class JournalEntryTag(models.Model):
  entry = models.ForeignKey(
    JournalEntry, related_name="journal_entry_tags", on_delete=models.CASCADE
  )
  tag = models.ForeignKey(
    Tag, related_name="journal_entry_tags", on_delete=models.CASCADE
  )

  def __str__(self):
    return self.tag.name
