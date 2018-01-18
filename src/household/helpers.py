from . import models

from django.db.models import OuterRef, Exists

def find_user_households(user):
  """
  Find households that a user is member of and thus allowed to look at.
  """

  memberships = models.HouseholdMembership.objects \
    .order_by() \
    .filter(household_id=OuterRef("pk"), user=user)

  households = models.Household.objects \
    .annotate(membership_exists=Exists(memberships)) \
    .filter(membership_exists=True)

  return households
