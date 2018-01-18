from . import decorators
from household.helpers import find_user_households
from journal.helpers import find_household_entries_for_user

from graphene import relay
import graphene

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

  @decorators.limited_pagination
  def resolve_households(user, info, *args, **kwargs):
    return find_user_households(user)
