from . import models

from django.http import HttpResponseForbidden

class AuthTokenMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    bearer = None
    response = None

    header = request.META.get("HTTP_AURHORIZATION")

    if type(header) is str:
      words = header.split(" ")

      if len(words) == 2 and words[0] == "Bearer":
        bearer = words[1]

    if bearer is None:
      cookie = request.COOKIES.get("mjoebearer")

      if type(cookie) is str:
        bearer = cookie

    if bearer is not None:
      auth_token = models.AuthToken.objects \
        .select_related("user") \
        .filter(token=bearer) \
        .first()

      if auth_token is None:
        response = HttpResponseForbidden()
      else:
        request.user = auth_token.user

    if response is None:
      response = self.get_response(request)

    return response
