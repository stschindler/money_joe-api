from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class AuthToken(models.Model):
  user = models.ForeignKey(
    User, related_name="auth_tokens", on_delete=models.CASCADE
  )
  token = models.CharField(max_length=128, unique=True)
  creation_time = models.DateTimeField()
  last_use_time = models.DateTimeField(blank=True, null=True, default=None)

  def __str__(self):
    return self.token

  def save(self, *args, **kwargs):
    if self.pk is None and self.creation_time is None:
      self.creation_time = timezone.now()

    return super().save(*args, **kwargs)
