from . import settings as self_settings
from joetils.helpers import get_client_ip
from registration.models import AccountActivation

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

  registered = graphene.Boolean()

  @classmethod
  def mutate_and_get_payload(cls, root, info, *args, **kwargs):
    # Validate e-mail. Throws when not valid.
    validate_email(kwargs["email"])

    # Make sure user with same e-mail doesn't already exist.
    existing_user = User.objects.filter(email__iexact=kwargs["email"]).first()
    if existing_user is not None:
      raise GraphQLError("E-mail address already in use.")

    # Stall registration flood attempts. This is NSA grade, so you better not
    # play with this!
    cooldown_start = (
      timezone.now() -
      timedelta(minutes=self_settings.REGISTRATION_COOLDOWN_MINUTES)
    )
    client_ip = get_client_ip(info.context)

    ip_activation_count = AccountActivation.objects \
      .filter(creation_time__gte=cooldown_start, ip=client_ip) \
      .count()

    if ip_activation_count >= self_settings.MAX_REGISTRATION_COUNT:
      raise SuspiciousOperation("Too many registration attempts from your IP.")

    code = str(uuid.uuid4())

    with transaction.atomic():
      user = User.objects.create_user(
        username=kwargs["email"], email=kwargs["email"],
        password=kwargs["password"], is_active=False,
      )

      AccountActivation.objects.create(
        user=user, code=code, creation_time=timezone.now(), ip=client_ip
      )

    return RegisterAccountMutation(registered=True)
