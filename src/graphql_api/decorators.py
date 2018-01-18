from . import settings as self_settings

def limited_pagination(func):
  """
  Decorator for limiting the `first` and `last` pagination parameters. Uses
  MJOE_DEFAULT_PAGE_SIZE and MJOE_MAX_PAGE_SIZE settings. Raises an exception
  when values are invalid rather than ignoring/fixing them.
  """

  def wrapper(*args, **kwargs):
    if "first" in kwargs and "last" in kwargs:
      raise RuntimeError("Use either `first` or `last`, not both.")

    for key in ("first", "last"):
      if key in kwargs:
        try:
          value = int(kwargs[key])
        except ValueError:
          raise ValueError("`{}` must be an integer.".format(key))

        if value < 0:
          raise ValueError("`{}` must be 0 or greater.".format(key))
        elif value > self_settings.MAX_PAGE_SIZE:
          raise ValueError("`{}` must not be greater than {}.".format(
            key, self_settings.MAX_PAGE_SIZE
          ))

        kwargs[key] = value
        break # Break out of for loop to skip `else` branch.

    else:
      kwargs["first"] = self_settings.DEFAULT_PAGE_SIZE

    result = func(*args, **kwargs)
    return result

  return wrapper

