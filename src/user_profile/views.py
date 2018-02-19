from . import helpers

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

import traceback

def make_error_response(text, status=400):
  return HttpResponse(text, content_type="text/plain", status=status)

class OptOutView(View):
  def get(self, request):
    token = request.GET.get("token")
    response = None

    if type(token) is not str:
      response = make_error_response("`token` must be string.")

    try:
      data = helpers.parse_opt_out_token(token)
    except helpers.OptOutTokenError:
      traceback.print_exc()
      response = make_error_response("JWT invalid.")

    user = User.objects.filter(id=data["user_id"]).first()

    if user is None:
      response = make_error_response("User not found.")

    if response is None:
      user.profile.email_opted_out = True
      user.profile.save()

      response = render(request, "user_profile/opt_out_successful.html")

    return response
