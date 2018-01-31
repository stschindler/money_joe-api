from django.conf import settings

MAX_REGISTRATION_COUNT = \
  getattr(settings, "MJOE_MAX_REGISTRATION_COUNT", 5)
REGISTRATION_COOLDOWN_MINUTES = \
  getattr(settings, "REGISTRATION_COOLDOWN_MINUTES", 15)
