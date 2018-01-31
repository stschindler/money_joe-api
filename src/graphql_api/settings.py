from django.conf import settings

DEFAULT_PAGE_SIZE = getattr(settings, "MJOE_DEFAULT_PAGE_SIZE", 10)
MAX_PAGE_SIZE = getattr(settings, "MJOE_MAX_PAGE_SIZE", 100)
