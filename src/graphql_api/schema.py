from . import types

import graphene

class Query(graphene.ObjectType):
  node = graphene.relay.Node.Field()
  me = graphene.Field(types.Me)

  def resolve_me(instance, info):
    return (
      info.context.user
      if info.context.user.is_authenticated is True
      else None
    )

schema = graphene.Schema(query=Query)
