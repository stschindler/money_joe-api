from . import decorators
from currency.models import Currency
from household.helpers import find_user_households

import graphene

class CurrencyNode(graphene.ObjectType):
  class Meta:
    interfaces = (graphene.relay.Node,)

  iso_code = graphene.String(required=True)
  symbol = graphene.String(required=True)

  @classmethod
  @decorators.node_resource
  def get_node(cls, info, id):
    result = None

    if info.context.user.is_authenticated is True:
      result = Currency.objects.filter(id=id).first()

    return result

class HouseholdNode(graphene.ObjectType):
  class Meta:
    interfaces = (graphene.relay.Node,)

  name = graphene.String(required=True)
  default_currency = graphene.Field(CurrencyNode, required=True)

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

class Me(graphene.ObjectType):
  class Meta:
    interfaces = (graphene.relay.Node,)

  username = graphene.String(required=True)
  email = graphene.String(required=True)

