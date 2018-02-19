from mail.helpers import send_template_mail

from django.conf import settings

import jwt

JWT_PRIVATE_KEY = getattr(settings, "JWT_PRIVATE_KEY")
JWT_PUBLIC_KEY = getattr(settings, "JWT_PUBLIC_KEY")

class OptOutTokenError(Exception): pass

def send_user_mail(user, *args, **kwargs):
  """Send an e-mail to a user if they haven't opted out.

  Forwards all arguments to `mail.helpers.send_template_mail`, except for
  `recipient_email`, which is taken from the user.
  """
  if user.profile.email_opted_out is False:
    send_template_mail(user.email, *args, **kwargs)

def create_opt_out_token(user_id):
  """Create JWT for opting out from receiving e-mails.
  """
  token = jwt.encode({"user_id": user_id}, JWT_PRIVATE_KEY, algorithm="RS256")
  return token

def parse_opt_out_token(token):
  try:
    data = jwt.decode(token, JWT_PUBLIC_KEY, algorithm="RS256")
  except Exception as error:
    raise OptOutTokenError(str(error))

  return data

