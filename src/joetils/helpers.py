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
