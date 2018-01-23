from django.conf import settings

DEFAULT_PAGE_SIZE = getattr(settings, "MJOE_DEFAULT_PAGE_SIZE", 10)
MAX_PAGE_SIZE = getattr(settings, "MJOE_MAX_PAGE_SIZE", 100)

MAX_REGISTRATION_COUNT = getattr(settings, "MJOE_MAX_REGISTRATION_COUNT", 5)
REGISTRATION_COOLDOWN_MINUTES = \
  int(getattr(settings, "MJOE_REGISTRATION_COOLDOWN_MINUTES", 30))
