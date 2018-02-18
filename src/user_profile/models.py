from geo.models import Language

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  user = models.OneToOneField(
    User, related_name="profile", on_delete=models.CASCADE
  )
  language = models.ForeignKey(
    Language, related_name="user_profiles", on_delete=models.CASCADE
  )
  email_opted_out = models.BooleanField(default=False)
