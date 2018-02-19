from . import models
from . import settings as self_settings

from django.core.mail import send_mail
from django.db.models import OuterRef, Exists, Q
import html2text

def _apply_fragments(body, fragments, custom_fragments=None):
  format_key = lambda key: "{" + key + "}"

  for fragment in fragments:
    body = body.replace(format_key(fragment.reference), fragment.body)

  if custom_fragments is not None:
    for key, value in custom_fragments.items():
      body = body.replace(format_key(key), value)

  return body

def send_template_mail(
  recipient_email, template_name, locale_name=None, custom_fragments=None
):
  """Build content from an e-mail template and send to recipient.

  `locale_name` can be `None` to use the fallback locale.

  If the requested locale isn't available, the fallback is used. If the
  fallback isn't available, MailTemplate.DoesNotExist is raised.
  """

  # Find requested template. Use fallback if not found.
  template_queryset = models.MailTemplate.objects \
    .filter(reference=template_name)

  template = template_queryset \
    .filter(language__locale_name=locale_name) \
    .first()

  if template is None and locale_name is not None:
    template = template_queryset.filter(language=None).first()

  if template is None:
    raise models.MailTemplate.DoesNotExist("locale_name={}".format(
      locale_name
    ))

  # If signature is requested, get the signature that matches the requested
  # locale. If none is found, use the fallback.
  if template.signature_included is True:
    signature = models.MailSignature.objects \
      .filter(language__locale_name=locale_name) \
      .first()

    if signature is None:
      signature = models.MailSignature.objects \
        .filter(language__locale_name=None) \
        .first()

  else:
    signature = None

  # Build signature body. Use fragments that match the signature's language or
  # act as fallbacks.
  if signature is None:
    signature_body = ""

  else:
    language_fragments = models.MailFragment.objects \
      .order_by() \
      .filter(
        reference=OuterRef("reference"),
        language=signature.language,
      )

    signature_fragments = models.MailFragment.objects \
      .annotate(language_fragment_exists=Exists(language_fragments)) \
      .filter(
        Q(language=signature.language) |
        Q(language=None, language_fragment_exists=False)
      )

    signature_body = \
      _apply_fragments(signature.body, signature_fragments, custom_fragments)

  # Build mail body. Use custom fragments and fragments that match the
  # template's language.
  template_fragments = models.MailFragment.objects \
    .filter(language=template.language)

  mail_body = \
    _apply_fragments(template.body, template_fragments, custom_fragments)
  mail_body += signature_body

  plain_body = html2text.html2text(mail_body)

  # Send out mail.
  send_mail(
    subject=template.subject,
    message=plain_body,
    from_email=self_settings.EMAIL_FROM_ADDRESS,
    recipient_list=(recipient_email,),
    html_message=mail_body,
  )
