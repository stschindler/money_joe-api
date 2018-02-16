from . import settings as self_settings
from geo.models import Language
from joetils.helpers import get_client_ip
from mail.helpers import send_template_mail
from registration.helpers import is_registration_count_exceeded
from registration.models import AccountActivation
from user_profile.models import UserProfile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, SuspiciousOperation
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone
from graphql import GraphQLError
import graphene

from datetime import timedelta
import uuid

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
      code = str(uuid.uuid4())

      with transaction.atomic():
        user = User.objects.create_user(
          username=kwargs["email"], email=kwargs["email"],
          password=kwargs["password"], is_active=False,
        )

        AccountActivation.objects.create(
          user=user, code=code, creation_time=timezone.now(), ip=client_ip
        )

        user_profile = UserProfile.objects.create(user=user, language=language)

        email_parameters = {
          "activation_url": "https://moneyjoe.io/",
        }

        send_template_mail(user.email, "registration_activation", locale_name)

    return RegisterAccountMutation(errors=errors)
