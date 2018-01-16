from . import types

import graphene

class Query(graphene.ObjectType):
  me = graphene.Field(types.MeType)

  def resolve_me(instance, info):
    return (
      info.context.user
      if info.context.user.is_authenticated is True
      else None
    )

schema = graphene.Schema(query=Query)
