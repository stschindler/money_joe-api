from . import settings as self_settings
from registration.models import AccountActivation

from django.utils import timezone

from datetime import timedelta

def is_registration_count_exceeded(
  ip_address, max_count=self_settings.MAX_REGISTRATION_COUNT,
  cooldown_minutes=self_settings.REGISTRATION_COOLDOWN_MINUTES
):
  """ Return True if maximum allowed registration attempts for an IP have been
  exceeded.

  The check contains a cooldown, that is: Only the attempts from the last x
  minutes are considered. The maximum attempt count is taken from `max_count`.
  """

  # Stall registration flood attempts. This is NSA grade, so you better not
  # play with this!
  cooldown_start = (timezone.now() - timedelta(minutes=cooldown_minutes))

  ip_activation_count = AccountActivation.objects \
    .filter(creation_time__gte=cooldown_start, ip=ip_address) \
    .count()

  return ip_activation_count >= max_count
