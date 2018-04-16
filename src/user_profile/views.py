from . import helpers, models

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

import traceback

def make_error_response(text, status=400):
  return HttpResponse(text, content_type="text/plain", status=status)

class OptOutView(View):
  def get(self, request):
    response = None
    token = request.GET.get("token")

    if type(token) is not str:
      response = make_error_response("`token` must be string.")

    if response is None:
      parsed_token = None

      try:
        parsed_token = helpers.parse_opt_out_token(token)
      except helpers.OptOutTokenError:
        traceback.print_exc()
        response = make_error_response("Token invalid.")

    if response is None:
      user_profile = models.UserProfile.objects \
        .select_related("user") \
        .filter(email_opt_out_code=parsed_token) \
        .first()

      if user_profile is None:
        response = make_error_response("User profile not found.")

    if response is None:
      user = user_profile.user
      user.profile.email_opted_out = True
      user.profile.save()

      response = render(request, "user_profile/opt_out_successful.html")

    return response
