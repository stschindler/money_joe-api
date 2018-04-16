from . import helpers, models
from joetils.helpers import get_client_ip, create_web_url

from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

import traceback

def make_error_response(text, status=400):
  return HttpResponse(text, content_type="text/plain", status=status)

class ActivateAccountView(View):
  def get(self, request):
    response = None
    token = request.GET.get("token")

    if type(token) is not str:
      response = make_error_response("`token` must be string.")

    try:
      data = helpers.parse_activation_token(token)
    except helpers.OptOutTokenError:
      traceback.print_exc()
      response = make_error_response("Token invalid.")

    account_activation = models.AccountActivation.objects \
      .select_related("user") \
      .filter(code=data, activation_time=None) \
      .first()

    if account_activation is None:
      response = make_error_response("Unused activation token not found.")

    if response is None:
      redirect_url = create_web_url()
      response = render(
        request, "registration/activation_successful.html",
        {"redirect_url": redirect_url}
      )

      user = account_activation.user

      with transaction.atomic():
        user.is_active = True
        user.save()

        account_activation.activation_time = timezone.now()
        account_activation.ip = get_client_ip(request)
        account_activation.save()

    return response
