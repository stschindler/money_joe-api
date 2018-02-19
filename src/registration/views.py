from . import helpers, models
from joetils.helpers import get_client_ip

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
      response = make_error_response("JWT invalid.")

    user = User.objects.filter(id=data["user_id"]).first()
    if user is None:
      response = make_error_response("User not found.")

    activation = models.AccountActivation.objects \
      .filter(user=user, activation_time=None) \
      .first()

    if activation is None:
      response = make_error_response("Activation code invalid/not found.")

    if response is None:
      with transaction.atomic():
        user.is_active = True
        user.save()

        activation.activation_time = timezone.now()
        activation.ip = get_client_ip(request)
        activation.save()

        response = render(request, "registration/activation_successful.html")

    return response
