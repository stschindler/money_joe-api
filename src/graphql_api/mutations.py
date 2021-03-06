from . import settings as self_settings, models, types
from currency.models import Currency
from geo.models import Language
from household.models import Household
from joetils.helpers import get_client_ip, create_api_url
from registration.helpers import create_activation_token
from registration.helpers import is_registration_count_exceeded
from registration.models import AccountActivation
from user_profile.helpers import parse_opt_out_token
from user_profile.helpers import send_user_mail, create_opt_out_token
from user_profile.models import UserProfile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, SuspiciousOperation
from django.core.validators import validate_email
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from graphql import GraphQLError
import graphene

from datetime import timedelta
import urllib
import uuid

class CreateHouseholdMutation(graphene.relay.ClientIDMutation):
  class Input:
    name = graphene.String(required=True)
    default_currency = graphene.ID(required=True)

  household = graphene.Field(types.HouseholdNode)
  errors = graphene.List(graphene.String)

  @classmethod
  def mutate_and_get_payload(cls, root, info, *args, **kwargs):
    errors = []
    household = None

    currency_node = graphene.Node.get_node_from_global_id(
      info, kwargs["default_currency"], only_type=types.CurrencyNode
    )

    if currency_node is None:
      errors.append("Currency not found.")

    if len(errors) < 1:
      household = Household.objects.create(
        name=kwargs["name"], default_currency_id=currency_node.id
      )

    return CreateHouseholdMutation(household=household, errors=errors)

class LoginMutation(graphene.relay.ClientIDMutation):
  class Input:
    username = graphene.String(required=True)
    password = graphene.String(required=True)

  token = graphene.String()
  errors = graphene.List(graphene.String)

  @classmethod
  def mutate_and_get_payload(cls, root, info, *args, **kwargs):
    errors = []
    token = None

    user = User.objects.filter(username__iexact=kwargs["username"]).first()

    if user is None or user.check_password(kwargs["password"]) is not True:
      errors.append("Username/password wrong.")

    elif user.is_active is not True:
      errors.append("User account not active/suspended.")

    else:
      token = str(uuid.uuid4())
      auth_token = models.AuthToken.objects.create(user=user, token=token)

    return LoginMutation(token=token, errors=errors)

class RegisterAccountMutation(graphene.relay.ClientIDMutation):
  class Input:
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    locale_name = graphene.String()

  errors = graphene.List(graphene.String)

  @classmethod
  def mutate_and_get_payload(cls, root, info, *args, **kwargs):
    errors = []

    try:
      validate_email(kwargs["email"])
      email_valid = True
    except ValidationError:
      errors.append("E-mail address invalid.")
      email_valid = False

    if len(kwargs["password"]) < 6:
      errors.append("Password too short, minimum is 6 chars.")

    if email_valid is True:
      existing_user = \
        User.objects.filter(email__iexact=kwargs["email"]).first()
      client_ip = get_client_ip(info.context)

      if existing_user is not None:
        errors.append("E-mail address already in use.")

      elif is_registration_count_exceeded(client_ip) is True:
        errors.append("Too many registration attempts from your IP.")

    # Use requested locale name.
    locale_name = None

    if "locale_name" in kwargs:
      language = Language.objects \
        .filter(locale_name=kwargs["locale_name"]) \
        .first()

      if language is None:
        errors.append("Invalid locale name: {}".format(kwargs["locale_name"]))

      locale_name = kwargs["locale_name"]

    if len(errors) < 1:
      with transaction.atomic():
        user = User.objects.create_user(
          username=kwargs["email"], email=kwargs["email"],
          password=kwargs["password"], is_active=False,
        )

        opt_out_token = create_opt_out_token(user.id)
        user_profile = UserProfile.objects.create(
          user=user, language=language, email_opt_out_code=opt_out_token
        )

        opt_out_url = create_api_url(
          reverse("user_profile_opt_out") +
          "?" + urllib.parse.urlencode({"token": opt_out_token})
        )

        activation_token = create_activation_token(user.id)
        AccountActivation.objects.create(
          user=user, creation_time=timezone.now(), ip=client_ip,
          code=activation_token,
        )
        activation_url = create_api_url(
          reverse("registration_activate_account") +
          "?" + urllib.parse.urlencode({"token": activation_token})
        )

        fragments = {
          "activation_url": activation_url,
          "optout_url": opt_out_url,
        }
        send_user_mail(user, "registration_activation", locale_name, fragments)

    return RegisterAccountMutation(errors=errors)
