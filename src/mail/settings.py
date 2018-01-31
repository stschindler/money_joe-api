from django.conf import settings

EMAIL_FROM_ADDRESS = getattr(settings, "EMAIL_FROM_ADDRESS", "hi@moneyjoe.io")
