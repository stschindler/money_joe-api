from ...models import Currency

from django.core.management import BaseCommand

import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    data = [
      {"iso_code": "EUR", "symbol": "€"},
      {"iso_code": "USD", "symbol": "$"},
      {"iso_code": "GBP", "symbol": "£"},
      {"iso_code": "SEK", "symbol": "SEK"},
    ]

    for row in data:
      currency = Currency.objects \
        .filter(iso_code=row["iso_code"]) \
        .first()

      if currency is None:
        currency = Currency(iso_code=row["iso_code"])

      for key, value in row.items():
        setattr(currency, key, value)

      currency.save()

      logger.info("Currency {} saved.".format(currency.iso_code))
