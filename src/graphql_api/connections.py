from . import types

import graphene

class HouseholdConnection(graphene.relay.Connection):
  class Meta:
    node = types.HouseholdNode

class CurrencyConnection(graphene.relay.Connection):
  class Meta:
    node = types.CurrencyNode
