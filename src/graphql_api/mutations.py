from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import graphene

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
      raise ValidationError("E-mail address already in use.")

    user = User.objects.create_user(
      username=kwargs["email"], email=kwargs["email"],
      password=kwargs["password"], is_active=False,
    )

    return RegisterAccountMutation(registered=True)
