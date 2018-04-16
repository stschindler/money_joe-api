from . import settings as self_settings

def node_resource(func):
  """
  Decorator for wrapping a returned resource into an already defined Graphene
  ObjectType. Use this decorator in front of `get_node()` implementations, then
  just return the resource and its properties will automagically be put into
  the proper ObjectType instance.

  The returned value can be an object or a dict.

  Remember to put a @classmethod before this decorator!
  """

  def wrapper(cls, info, id, *args, **kwargs):
    result = func(cls, info, id, *args, **kwargs)
    node_args = {}

    for field_name, field in cls._meta.fields.items():
      if isinstance(result, dict) is True:
        node_args[field_name] = result[field_name]
      elif isinstance(result, object) is True:
        node_args[field_name] = getattr(result, field_name, None)
      else:
        raise NotImplementedError("Result must be dict or object.")

    return cls(**node_args)

  return wrapper

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
