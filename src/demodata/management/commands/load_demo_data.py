from account.models import Account
from currency.models import Currency, CountryCurrency
from geo.models import Country, Language
from household.models import Household, HouseholdMembership
from mail.models import MailSignature, MailFragment, MailTemplate

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
        "email": "hi@stschindler.io", "is_staff": True, "is_superuser": True,
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
    languages = {}

    for language_data in languages_data:
      language = \
        find_or_prepare(Language, locale_name=language_data["locale_name"])

      set_field_values(language, language_data)
      language.country = countries[language_data["country_ref"]]
      language.save()

      languages[language.locale_name] = language

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
      household = households[household_membership_data["household_ref"]]
      user = users[household_membership_data["user_ref"]]

      household_membership = find_or_prepare(
        HouseholdMembership, household=household, user=user
      )

      set_field_values(household_membership, household_membership_data)
      household_membership.save()

    # Accounts.
    accounts_data = [
      {
        "household_ref": "Schindler", "reference": "DE123456789X",
        "name": "Stefan's giro account", "owner_ref": "stsch",
        "meta": {"bic": "BINGDIDING"},
      },
      {
        "household_ref": "Schindler", "reference": "DE44556677X",
        "name": "Holiday savings", "owner_ref": "tisch",
        "meta": {"bic": "WOOMDIBOOM"},
      },
      {
        "household_ref": "Swiss", "reference": "CH23984948352943X",
        "name": "Secret account", "owner_ref": "stsch",
        "meta": {"bic": "CHOCOLATE"},
      },
    ]

    for account_data in accounts_data:
      household = households[account_data["household_ref"]]
      owner = users[account_data["owner_ref"]]

      account = find_or_prepare(
        Account, household=household, reference=account_data["reference"]
      )

      set_field_values(account, account_data)
      account.owner = owner
      account.save()

    # Mail signatures.
    mail_signatures_data = [
      {
        "language_ref": None,
        "body": """
<p>
  You are receiving this e-mail because you are a user of MoneyJoe, the hipster
  housekeeping tool. If you think you've wrongly received it, or generally
  don't want to receive mails from us, just click the following link and we
  won't bother you again with any e-mail:
</p>

<p><a href="{optout_url}">{optout_url}</a></p>

<p>
  <strong>Want to reach out to us?</strong> Go to
  <a href="{product_website_url}">{product_website_url</a>, tweet
  to <a href="{contact_twitter_handle}">{contact_twitter_handle}</a> or send an
  e-mail to <a href="{contact_email_address}">{contact_email_address}</a>!
</p>

<p>
  MoneyJoe is a Limbozz product.
  (<a href="{limbozz_website_url}">{limbozz_website_url}</a>)
</p>

{impressum}
        """.strip(),
      },
      {
        "language_ref": "de_de",
        "body": """
<p>
  Du erhälst diese E-Mail, weil du ein User von MoneyJoe bist, dem
  Hipster-Haushaltsbuch-Tool. Wenn du der Meinung bist, dass du die Mail
  fälschlicherweise bekommen hast, oder generell keine Lust auf Mails von uns
  hast, dann klicke den folgenden Link:
</p>

<p><a href="{optout_url}">{optout_url}</a></p>

<p>
  <strong>Hast du uns was mitzuteilen?</strong> Gehe zu
  <a href="{product_website_url}">{product_website_url}</a>, tweete an
  <a href="{contact_twitter_handle}">{contact_twitter_handle}</a>
  oder sende eine E-Mail zu
  <a href="{contact_email_address}">{contact_email_address}</a>!
</p>

<p>
  MoneyJoe ist ein Produkt von Limbozz
  (<a href="{limbozz_website_url}">{limbozz_website_url}</a>).
</p>

{impressum}
        """.strip(),
      },
    ]

    for mail_signature_data in mail_signatures_data:
      language = (
        languages[mail_signature_data["language_ref"]]
        if mail_signature_data["language_ref"] is not None
        else None
      )

      mail_signature = find_or_prepare(MailSignature, language=language)

      set_field_values(mail_signature, mail_signature_data)
      mail_signature.save()

    # Mail fragments.
    mail_fragments_data = [
      {
        "reference": "product_website_url",
        "language_ref": None,
        "body": "https://moneyjoe.io/",
      },
      {
        "reference": "contact_email_address",
        "language_ref": None,
        "body": "hi@moneyjoe.io",
      },
      {
        "reference": "contact_twitter_handle",
        "language_ref": None,
        "body": "@MoneyJoeApp",
      },
      {
        "reference": "limbozz_website_url",
        "language_ref": None,
        "body": "https://limbozz.com/",
      },

      {
        "reference": "impressum",
        "language_ref": None,
        "body": """
<p>Impressum (Legal Notice)</p>

<address>
  <strong>Limbozz GmbH</strong><br>
  Pfarrer-Becking-Straße 21<br>
  46397 Bocholt<br>
  Deutschland
</address>

<ul>
  <li>Phone: +49 (2871) 2424436</li>
  <li>Fax: +49 (2871) 2424437</li>
  <li>E-Mail: hi@limbozz.com</li>
</ul>

<ul>
  <li>Management: Stefan Schindler</li>
  <li>Commercial Register: Amtsgericht Coesfeld, HRB 15916</li>
  <li>VAT ID (USt-IdNr.): DE304363536</li>
  <li>Responsible according to § 55 Abs. 2 RStV: Stefan Schindler</li>
</ul>
        """.strip(),
      },

      {
        "reference": "impressum",
        "language_ref": "de_de",
        "body": """
<p>Impressum</p>

<address>
  <strong>Limbozz GmbH</strong><br>
  Pfarrer-Becking-Straße 21<br>
  46397 Bocholt<br>
  Deutschland
</address>

<ul>
  <li>Telefon: +49 (2871) 2424436</li>
  <li>Fax: +49 (2871) 2424437</li>
  <li>E-Mail: hi@limbozz.com</li>
</ul>

<ul>
  <li>Geschäftsführung: Stefan Schindler</li>
  <li>Handelsregister: Amtsgericht Coesfeld, HRB 15916</li>
  <li>USt-IdNr.: DE304363536</li>
  <li>Verantwortlicher gemäß § 55 Abs. 2 RStV: Stefan Schindler</li>
</ul>
        """.strip(),
      },
    ]

    for mail_fragment_data in mail_fragments_data:
      language = (
        languages[mail_fragment_data["language_ref"]]
        if mail_fragment_data["language_ref"] is not None
        else None
      )

      mail_fragment = find_or_prepare(
        MailFragment, reference=mail_fragment_data["reference"],
        language=language,
      )

      set_field_values(mail_fragment, mail_fragment_data)
      mail_fragment.save()

    # Mail templates.
    mail_templates_data = [
      {
        "reference": "registration_activation",
        "language_ref": None,
        "subject": "One more step ahead: Activate your account now!",
        "signature_included": True,
        "body": """
<p>Dear user!</p>
<p>
  Your MoneyJoe account was created. In order to use it please activate your
  account and validate your e-mail address by clicking on the following link:
</p>
<p><a href="{activation_url}">{activation_url}</a></p>
<p>Thanks &amp; and have fun!</p>
        """.strip(),
      },

      {
        "reference": "registration_activation",
        "language_ref": "de_de",
        "subject": "Nur noch ein Schritt: Aktiviere jetzt deinen Account!",
        "signature_included": True,
        "body": """
<p>Lieber User!</p>
<p>
  Dein MoneyJoe-Account wurde erstellt. Damit du ihn nutzen kannst, musst du
  nur noch deinen Account aktivieren und deine E-Mail-Adresse bestätigen.
  Klicke dazu einfach auf folgenden Link:
</p>
<p><a href="{activation_url}">{activation_url}</a></p>
<p>Danke &amp; viel Spaß!</p>
        """.strip(),
      },
    ]

    for mail_template_data in mail_templates_data:
      language = (
        languages[mail_template_data["language_ref"]]
        if mail_template_data["language_ref"] is not None
        else None
      )

      mail_template = find_or_prepare(
        MailTemplate, language=language,
        reference=mail_template_data["reference"],
      )

      set_field_values(mail_template, mail_template_data)
      mail_template.save()
