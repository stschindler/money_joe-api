from currency.models import Currency, CountryCurrency
from geo.models import Country, Language

from django.core.exceptions import FieldDoesNotExist
from django.core.management import BaseCommand

def set_field_values(instance, data):
  for key, value in data.items():
    try:
      field = instance._meta.get_field(key)
    except FieldDoesNotExist:
      field = None

    if field is not None:
      setattr(instance, key, value)

def find_or_prepare(model, **kwargs):
  instance = model.objects.filter(**kwargs).first()

  if instance is None:
    instance = model(**kwargs)

  return instance

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    # Countries.
    countries_data = [
      {"iso_code": "de", "name": "Germany"},
      {"iso_code": "ch", "name": "Switzerland"},
      {"iso_code": "us", "name": "United States of America"},
    ]
    countries = {}

    for country_data in countries_data:
      country = find_or_prepare(Country, iso_code=country_data["iso_code"])

      set_field_values(country, country_data)
      country.save()

      countries[country.iso_code] = country

    # Languages.
    languages_data = [
      {"locale_name": "de_de", "name": "German", "country_ref": "de"},
      {"locale_name": "de_ch", "name": "German (Swiss)", "country_ref": "ch"},
      {"locale_name": "en_us", "name": "English (US)", "country_ref": "us"},
    ]

    for language_data in languages_data:
      language = \
        find_or_prepare(Language, locale_name=language_data["locale_name"])

      set_field_values(language, language_data)
      language.country = countries[language_data["country_ref"]]
      language.save()

    # Currencies.
    currencies_data = [
      {"iso_code": "EUR", "symbol": "€"},
      {"iso_code": "CHF", "symbol": "Fr."},
      {"iso_code": "USD", "symbol": "US$"},
    ]
    currencies = {}

    for currency_data in currencies_data:
      currency = find_or_prepare(Currency, iso_code=currency_data["iso_code"])

      set_field_values(currency, currency_data)
      currency.save()

      currencies[currency.iso_code] = currency

    # Country currencies.
    country_currencies_data = [
      {"country_ref": "de", "currency_ref": "EUR"},
      {"country_ref": "ch", "currency_ref": "CHF"},
      {"country_ref": "us", "currency_ref": "USD"},
    ]

    for country_currency_data in country_currencies_data:
      country = countries[country_currency_data["country_ref"]]
      currency = currencies[country_currency_data["currency_ref"]]

      country_currency = find_or_prepare(
        CountryCurrency,
        country=country, currency=currency
      )
      set_field_values(country_currency, country_currency_data)
      country_currency.save()
