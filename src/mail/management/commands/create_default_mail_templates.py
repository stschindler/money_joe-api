from ... import models

from django.core.management import BaseCommand
from django.db import transaction

class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    data = {
      "en_us": {
        "activation_request": {
          "subject": "One more step ahead: Activate your account now!",

          "body": """Dear user!

Your MoneyJoe account was created. In order to use it, you have only have to
activate your account by validating your e-mail address.

Click on the following link to validate your e-mail address:

  [{url}]({url})

Thank you, and have fun!""",
        },

        "signature": {
          "subject": "Signature",

          "body": """MoneyJoe is a product of Limbozz (limbozz.com)

You are receiving this e-mail because you are a user of MoneyJoe, the
housekeeping tool ({website_url}).

If you falsely received this mail, or you don't want to receive any more
e-mails to this address in the future, then please click on this link:
{optout_url}

Contact:

  * E-Mail: {contact_email}
  * Twitter: {twitter_handle}
  * Web: {website_url}
  * Postal: {postal_address}""",
        },
      },
    }

    with transaction.atomic():
      models.MailTemplate.objects.create(
      )
