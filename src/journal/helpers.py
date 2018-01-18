from . import models
from household.models import HouseholdMembership

def find_household_entries_for_user(household_id, user_id):
  """
  Find all journal entries of a household a specific user is allowed to see.
  """
  entries = []

  membership = HouseholdMembership.objects \
    .filter(household_id=household_id, user_id=user_id) \
    .first()

  if membership is not None:
    entries = models.JournalEntry.objects \
      .filter(household_id=household_id)

  return entries
