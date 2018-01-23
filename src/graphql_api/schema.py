from . import decorators, types, mutations, connections
from household.helpers import find_user_households
from journal.helpers import find_household_entries_for_user

import graphene

class Mutation(graphene.ObjectType):
  register_account = mutations.RegisterAccountMutation.Field()

class Query(graphene.ObjectType):
  node = graphene.relay.Node.Field()
  me = graphene.Field(types.Me)
  households = graphene.relay.ConnectionField(connections.HouseholdConnection)

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

schema = graphene.Schema(query=Query, mutation=Mutation)
