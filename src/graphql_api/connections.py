from . import types

import graphene

class HouseholdConnection(graphene.relay.Connection):
  class Meta:
    node = types.HouseholdNode
