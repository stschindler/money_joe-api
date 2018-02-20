from account.models import Account
from currency.models import Currency, CountryCurrency
from geo.models import Country, Language
from graphql_api.models import AuthToken
from household.models import Household, HouseholdMembership
from journal.models import JournalEntry, JournalEntryTag
from mail.models import MailSignature, MailFragment, MailTemplate
from registration.models import AccountActivation
from tag.models import Tag
from user_profile.models import UserProfile

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
        "email": "moneyjoe.tina@stschindler.io", "first_name": "Tina",
        "last_name": "Schindler",
      },
      {
        "username": "johndoe", "password_raw": "jonnydonny",
        "email": "moneyjoe.johndoe@stschindler.io", "first_name": "John",
        "last_name": "Doe",
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
        "household_ref": "Schindler", "name": "Stefan's giro",
        "owner_ref": "stsch",
        "meta": {"iban": "DE123456789X", "bic": "BINGDIDING"},
      },
      {
        "household_ref": "Schindler", "name": "Holiday savings",
        "owner_ref": "stsch",
        "meta": {"iban": "DE44556677X", "bic": "WOOMDIBOOM"},
      },
      {
        "household_ref": "Schindler", "name": "Tina's wallet",
        "owner_ref": "tisch", "meta": {},
      },
      {
        "household_ref": "Swiss", "name": "Secret account",
        "owner_ref": "stsch",
        "meta": {"iban": "CH23984948352943X", "bic": "CHOCOLATE"},
      },
    ]
    accounts = {}

    for account_data in accounts_data:
      household = households[account_data["household_ref"]]
      owner = users[account_data["owner_ref"]]

      account = find_or_prepare(
        Account, household=household, name=account_data["name"]
      )

      set_field_values(account, account_data)
      account.owner = owner
      account.save()

      accounts[(household.name, account.name)] = account

    # Mail signatures.
    mail_signatures_data = [
      {
        "language_ref": None,
        "body": """
<hr>

<div style="color: #666; font-size: x-small;">
  <p>
    You are receiving this e-mail because you are a user of MoneyJoe, the awesome
    housekeeping tool. If you think you've wrongly received it, or generally
    don't want to receive mails from us, just
    <a href="{optout_url}">click here</a> and we won't bother you again with
    any e-mail.
  </p>

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
</div>
        """.strip(),
      },
      {
        "language_ref": "de_de",
        "body": """
<hr>

<div style="color: #666; font-size: x-small;">
  <p>
    Du erhälst diese E-Mail, weil du ein User von MoneyJoe bist, dem praktischen
    Haushaltsbuch. Wenn du meinst, dass du die Mail fälschlicherweise bekommen
    hast, oder generell keine Lust auf Mails von uns hast, dann
    <a href="{optout_url}">klicke hier</a>.
  </p>

  <p>
    <strong>Hast du uns etwas mitzuteilen?</strong> Gehe zu
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
</div>
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
  Blücherstraße 18<br>
  46397 Bocholt<br>
  Deutschland
</address>

<p>
  Phone: +49 (2871) 2424436<br>
  Fax: +49 (2871) 2424437<br>
  E-Mail: hi@limbozz.com
</p>

<p>
  Management: Stefan Schindler<br>
  Commercial register: Coesfeld, HRB 15916<br>
  VAT ID: DE304363536<br>
  Responsible according to § 55 Abs. 2 RStV: Stefan Schindler
</p>
        """.strip(),
      },

      {
        "reference": "impressum",
        "language_ref": "de_de",
        "body": """
<p>Impressum</p>

<address>
  <strong>Limbozz GmbH</strong><br>
  Blücherstraße 18<br>
  46397 Bocholt<br>
  Deutschland
</address>

<p>
  Telefon: +49 (2871) 2424436<br>
  Fax: +49 (2871) 2424437<br>
  E-Mail: hi@limbozz.com
</p>

<p>
  Geschäftsführung: Stefan Schindler<br>
  Handelsregister: Coesfeld, HRB 15916<br>
  USt-IdNr.: DE304363536<br>
  Verantwortlicher gemäß § 55 Abs. 2 RStV: Stefan Schindler
</p>
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
<p><a href="{activation_url}">Activate your account now!</a></p>
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
<p><a href="{activation_url}">Account jetzt aktivieren!</a></p>
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

    # Account activations.
    account_activations_data = [
      {
        "user_ref": "stsch", "creation_time": "2018-01-28T20:50:05+01:00",
        "activation_time": "2018-01-28T20:51:31+01:00", "ip": "127.0.0.1",
      },
      {
        "user_ref": "tisch", "creation_time": "2018-01-29T20:50:05+01:00",
        "activation_time": "2018-01-29T20:51:31+01:00", "ip": "192.168.1.10",
      },
      {
        "user_ref": "johndoe", "creation_time": "2018-01-29T12:13:14+01:00",
        "activation_time": None, "ip": "192.168.178.1",
      },
    ]

    for account_activation_data in account_activations_data:
      user = users[account_activation_data["user_ref"]]

      account_activation = find_or_prepare(AccountActivation, user=user)

      set_field_values(account_activation, account_activation_data)
      account_activation.save()

    # Auth tokens.
    auth_tokens_data = [
      {
        "user_ref": "stsch", "token": "a14fc0dc-fe58-41de-86d4-95943b155f3e",
        "creation_time": "2018-02-20T11:10:05+01:00", "last_use_time": None,
      },
      {
        "user_ref": "tisch", "token": "83d10fe3-239c-489c-898e-495543219a83",
        "creation_time": "2018-02-19T11:10:05+01:00",
        "last_use_time": "2018-02-20T10:02:44+01:00",
      },
    ]

    for auth_token_data in auth_tokens_data:
      user = users[auth_token_data["user_ref"]]

      auth_token = find_or_prepare(AuthToken, token=auth_token_data["token"])

      set_field_values(auth_token, auth_token_data)
      auth_token.user = user
      auth_token.save()

    # Tags.
    tags_data = [
      {"name": "Lebensmittel", "household_ref": "Schindler"},
      {"name": "Sprit", "household_ref": "Schindler"},
      {"name": "Schöggu", "household_ref": "Swiss"},
      {"name": "Herrgöttli", "household_ref": "Swiss"},
    ]

    for tag_data in tags_data:
      household = households[tag_data["household_ref"]]

      tag = find_or_prepare(Tag, name=tag_data["name"], household=household)

      set_field_values(tag, tag_data)
      tag.save()

    # Journal entries.
    journal_entries_data = [
      {
        "description": "Groceries (cash)",
        "creation_time": "2018-01-03T14:03:33+01:00",
        "booking_time": "2018-01-03T14:01:05+01:00",
        "valuta_time": "2018-01-03T14:01:05+01:00",
        "creator_ref": "tisch",
        "household_ref": "Schindler",
        "debit_account_ref": "Tina's wallet",
        "credit_account_ref": None,
        "value": 5839,
        "currency_ref": "EUR",
      },
      {
        "description": "Gas (bank wire)",
        "creation_time": "2018-01-04T14:03:33+01:00",
        "booking_time": "2018-01-04T14:01:05+01:00",
        "valuta_time": None,
        "creator_ref": "tisch",
        "household_ref": "Schindler",
        "debit_account_ref": "Stefan's giro",
        "credit_account_ref": None,
        "value": 3499,
        "currency_ref": "EUR",
      },
      {
        "description": "Donation",
        "creation_time": "2018-01-05T14:03:33+01:00",
        "booking_time": "2018-01-05T14:01:05+01:00",
        "valuta_time": "2018-01-05T14:01:05+01:00",
        "creator_ref": "stsch",
        "household_ref": "Schindler",
        "debit_account_ref": None,
        "credit_account_ref": "Stefan's giro",
        "value": 550,
        "currency_ref": "EUR",
      },
      {
        "description": "Transfer",
        "creation_time": "2018-01-06T14:03:33+01:00",
        "booking_time": "2018-01-06T14:01:05+01:00",
        "valuta_time": "2018-01-08T15:22:05+01:00",
        "creator_ref": "stsch",
        "household_ref": "Schindler",
        "debit_account_ref": "Stefan's giro",
        "credit_account_ref": "Holiday savings",
        "value": 1000,
        "currency_ref": "EUR",
      },

      {
        "description": "Whatever",
        "creation_time": "2018-02-06T14:03:33+01:00",
        "booking_time": "2018-02-06T14:01:05+01:00",
        "valuta_time": "2018-02-08T15:22:05+01:00",
        "creator_ref": "stsch",
        "household_ref": "Swiss",
        "debit_account_ref": None,
        "credit_account_ref": "Secret account",
        "value": 99999,
        "currency_ref": "CHF",
      },
    ]
    journal_entries = {}

    for journal_entry_data in journal_entries_data:
      creator = users[journal_entry_data["creator_ref"]]
      household = households[journal_entry_data["household_ref"]]
      currency = currencies[journal_entry_data["currency_ref"]]

      debit_account = (
        accounts[(
          journal_entry_data["household_ref"],
          journal_entry_data["debit_account_ref"],
        )]
        if journal_entry_data["debit_account_ref"] is not None
        else None
      )
      credit_account = (
        accounts[(
          journal_entry_data["household_ref"],
          journal_entry_data["credit_account_ref"],
        )]
        if journal_entry_data["credit_account_ref"] is not None
        else None
      )

      journal_entry = find_or_prepare(
        JournalEntry, household=household,
        description=journal_entry_data["description"]
      )

      set_field_values(journal_entry, journal_entry_data)
      journal_entry.debit_account = debit_account
      journal_entry.credit_account = credit_account
      journal_entry.currency = currency
      journal_entry.creator = creator
      journal_entry.save()

      journal_entries[(journal_entry.description, household.name)] = \
        journal_entry

    journal_entry_tags_data = [
      {
        "entry_ref": ("Groceries (cash)", "Schindler"),
      },
    ]

    # User profiles.
    user_profiles_data = [
      {"user_ref": "stsch", "language_ref": "de_de", "email_opted_out": False},
      {"user_ref": "tisch", "language_ref": "de_de", "email_opted_out": False},
      {
        "user_ref": "johndoe", "language_ref": "en_us",
        "email_opted_out": True,
      },
    ]

    for user_profile_data in user_profiles_data:
      user = users[user_profile_data["user_ref"]]
      language = languages[user_profile_data["language_ref"]]

      user_profile = find_or_prepare(UserProfile, user=user)

      set_field_values(user_profile, user_profile_data)
      user_profile.language = language
      user_profile.save()
