from django.conf import settings

def get_client_ip(request):
  """
  Get client IP from "X-Forwarded-For" HTTP header. If it's not set
  "REMOTE_ADDR" is used.
  """
  if "HTTP_X_FORWARDED_FOR" in request.META:
    client_ip = request.META["HTTP_X_FORWARDED_FOR"].split(",")[0]
  else:
    client_ip = request.META["REMOTE_ADDR"]

  return client_ip

def get_relative_url(path):
  index = 0

  for index, ch in enumerate(path):
    if ch != "/":
      break

  return path[index:]

def create_web_url(path="/"):
  assert(
    settings.WEB_URL.endswith("/") is False,
    "WEB_URL mustn't end with a slash."
  )
  assert(
    path.startswith("/") is True,
    "path must start with a slash: {}".format(path)
  )
  return settings.WEB_URL + path

def create_api_url(path="/"):
  assert(
    settings.API_URL.endswith("/") is False,
    "API_URL mustn't end with a slash."
  )
  assert(
    path.startswith("/") is True,
    "path must start with a slash: {}".format(path)
  )
  return settings.API_URL + path

def create_cdn_url(path="/"):
  assert(
    settings.CDN_URL.endswith("/") is False,
    "CDN_URL mustn't end with a slash."
  )
  assert(
    path.startswith("/") is True,
    "path must start with a slash: {}".format(path)
  )
  return settings.CDN_URL + path
