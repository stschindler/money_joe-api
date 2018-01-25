from geo.models import Country, Language

from django.core.exceptions import FieldDoesNotExist
from django.core.management import BaseCommand

def set_field_values(data, instance):
  for key, value in data.items():
    try:
      field = instance._meta.get_field(key)
    except FieldDoesNotExist:
      field = None

    if field is not None:
      setattr(instance, key, value)

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
      country = Country.objects \
        .filter(iso_code=country_data["iso_code"]) \
        .first()

      if country is None:
        country = Country(iso_code=country_data["iso_code"])

      set_field_values(country_data, country)
      country.save()

      countries[country.iso_code] = country

    # Languages.
    languages_data = [
      {"locale_name": "de_de", "name": "German", "country_ref": "de"},
      {"locale_name": "de_ch", "name": "German (Swiss)", "country_ref": "ch"},
      {"locale_name": "en_us", "name": "English (US)", "country_ref": "us"},
    ]

    for language_data in languages_data:
      language = Language.objects \
        .filter(locale_name=language_data["locale_name"]) \
        .first()

      if language is None:
        language = Language(locale_name=language_data["locale_name"])

      set_field_values(language_data, language)
      language.country = countries[language_data["country_ref"]]
      language.save()
