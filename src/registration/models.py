from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class AccountActivation(models.Model):
  user = models.OneToOneField(
    User, related_name="account_activations", on_delete=models.CASCADE,
    unique=True,
  )
  code = models.CharField(max_length=128, unique=True)
  creation_time = models.DateTimeField()
  activation_time = models.DateTimeField(blank=True, null=True, default=None)
  ip = models.CharField(max_length=128)

  def save(self, *args, **kwargs):
    if self.pk is None and self.creation_time is None:
      self.creation_time = timezone.now()

    return super().save(*args, **kwargs)

  def __str__(self):
    return str(self.user)
