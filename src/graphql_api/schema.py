from . import decorators
from household.helpers import find_user_households
from journal.helpers import find_household_entries_for_user

import graphene

class Household(graphene.ObjectType):
  class Meta:
    interfaces = (graphene.relay.Node,)

  name = graphene.String(required=True)

  @classmethod
  @decorators.node_resource
  def get_node(cls, info, id):
    result = None

    if info.context.user.is_authenticated is True:
      household = find_user_households(info.context.user) \
        .filter(id=id) \
        .first()

      if household is not None:
        result = household

    return result

class HouseholdConnection(graphene.relay.Connection):
  class Meta:
    node = Household

class Me(graphene.ObjectType):
  class Meta:
    interfaces = (graphene.relay.Node,)

  username = graphene.String(required=True)
  email = graphene.String(required=True)

class Query(graphene.ObjectType):
  node = graphene.relay.Node.Field()
  me = graphene.Field(Me)
  households = graphene.relay.ConnectionField(HouseholdConnection)

  def resolve_me(instance, info):
    return (
      info.context.user
      if info.context.user.is_authenticated is True
      else None
    )

  @decorators.limited_pagination
  def resolve_households(instance, info, *args, **kwargs):
    households = []

    if info.context.user.is_authenticated is True:
      households = find_user_households(info.context.user)

    return households

schema = graphene.Schema(query=Query)
