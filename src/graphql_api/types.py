import graphene

class MeType(graphene.ObjectType):
  username = graphene.String()
  email = graphene.String()
