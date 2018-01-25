from currency.models import Currency, CountryCurrency
from geo.models import Country, Language
from household.models import Household, HouseholdMembership

from django.contrib.auth.models import User
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
    # Users.
    users_data = [
      {
        "username": "stsch", "password_raw": "roflcopter",
        "email": "hi@stschindler.io", "is_staff": True, "is_admin": True,
        "first_name": "Stefan", "last_name": "Schindler",
      },
      {
        "username": "tisch", "password_raw": "miabambina",
        "email": "christianeschindler86@gmail.com", "first_name": "Tina",
        "last_name": "Schindler",
      },
    ]
    users = {}

    for user_data in users_data:
      user = find_or_prepare(User, username=user_data["username"])

      set_field_values(user, user_data)

      # Only set password if the user is new. Otherwise all active sessions
      # will be terminated, which is annoying when developing. :-)
      if user.pk is None:
        user.set_password(user_data["password_raw"])

      user.save()

      users[user.username] = user

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

    # Households.
    households_data = [
      {"name": "Schindler", "default_currency_ref": "EUR"},
      {"name": "Swiss", "default_currency_ref": "CHF"},
    ]
    households = {}

    for household_data in households_data:
      default_currency = currencies[household_data["default_currency_ref"]]

      household = find_or_prepare(Household, name=household_data["name"])

      set_field_values(household, household_data)
      household.default_currency = default_currency
      household.save()

      households[household.name] = household

    # Household memberships.
    household_memberships_data = [
      {
        "household_ref": "Schindler", "user_ref": "stsch",
        "level": HouseholdMembership.Level.ADMIN,
      },
      {
        "household_ref": "Schindler", "user_ref": "tisch",
        "level": HouseholdMembership.Level.USER,
      },
      {
        "household_ref": "Swiss", "user_ref": "stsch",
        "level": HouseholdMembership.Level.ADMIN,
      },
    ]

    for household_membership_data in household_memberships_data:
      household_membership = find_or_prepare(
          # TODO
      )
