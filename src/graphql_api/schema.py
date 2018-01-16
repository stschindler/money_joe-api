import graphene

class Query(graphene.ObjectType):
  hello_world = graphene.String()

  def resolve_hello_world(info, request):
    return "Hello World"

schema = graphene.Schema(query=Query)
