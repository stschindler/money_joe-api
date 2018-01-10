from django.contrib.auth.models import User
from django.db import models

class Household(models.Model):
  name = models.CharField(max_length=128)

  def __str__(self):
    return self.name

class HouseholdMembership(models.Model):
  class Level:
    ADMIN = 0
    USER = 1

  LEVEL_CHOICES = (
    (Level.ADMIN, "Admin"),
    (Level.USER, "User"),
  )

  household = models.ForeignKey(
    Household, related_name="memberships", on_delete=models.CASCADE
  )
  user = models.ForeignKey(
    User, related_name="household_memberships", on_delete=models.CASCADE
  )
  level = \
    models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=Level.USER)

  def __str__(self):
    return str(self.id)

