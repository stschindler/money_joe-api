from mail.helpers import send_template_mail

from django.conf import settings

import uuid

class OptOutTokenError(Exception): pass

def send_user_mail(user, *args, **kwargs):
  """Send an e-mail to a user if they haven't opted out.

  Forwards all arguments to `mail.helpers.send_template_mail`, except for
  `recipient_email`, which is taken from the user.
  """
  if user.profile.email_opted_out is False:
    send_template_mail(user.email, *args, **kwargs)

def create_opt_out_token(user_id):
  """Create token for opting out from receiving e-mails."""
  return str(uuid.uuid4())

def parse_opt_out_token(token):
  return token
