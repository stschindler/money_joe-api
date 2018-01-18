from . import settings as self_settings
from household.helpers import find_user_households
from journal.helpers import find_household_entries_for_user

from django.db.models import OuterRef, Exists
from django.db.models.query import QuerySet
from graphene import relay
import graphene

import base64
import collections

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
      print("Default first")
      kwargs["first"] = self_settings.DEFAULT_PAGE_SIZE

    from pprint import pprint
    pprint(kwargs)

    result = func(*args, **kwargs)
    return result

  return wrapper

#class Currency(graphene.ObjectType):
#  iso_code = graphene.String(required=True)
#  symbol = graphene.String(required=True)
#
#class JournalEntry(graphene.ObjectType):
#  description = graphene.String()
#  creation_time = graphene.types.datetime.DateTime(required=True)
#  booking_time = graphene.types.datetime.DateTime(required=True)
#  valuta_time = graphene.types.datetime.DateTime(required=True)
#  value = graphene.Int(required=True)
#  currency = graphene.Field(Currency, required=True)
#
#class JournalEntryConnection(relay.Connection):
#  class Meta:
#    node = JournalEntry

class Household(graphene.ObjectType):
  class Meta:
    interfaces = (relay.Node,)

  name = graphene.String(required=True)
#  default_currency = graphene.Field(Currency, required=True)
#  journal_entries = relay.ConnectionField(JournalEntryConnection)
#
#  def resolve_journal_entries(household, info):
#    return find_household_entries_for_user(household.id, info.context.user.id)

class HouseholdConnection(relay.Connection):
  class Meta:
    node = Household

class Me(graphene.ObjectType):
  username = graphene.String(required=True)
  email = graphene.String(required=True)

  households = relay.ConnectionField(HouseholdConnection)

  @limited_pagination
  def resolve_households(user, info, *args, **kwargs):
    return find_user_households(user)
