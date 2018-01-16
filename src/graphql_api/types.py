import graphene

class OwnerJournalEntryType(graphene.ObjectType):
  description = graphene.String()
  creation_time = graphene.types.datetime.DateTime(required=True)
  booking_time = graphene.types.datetime.DateTime(required=True)
  valuta_time = graphene.types.datetime.DateTime(required=True)
  value = graphene.Int(required=True)
  #currency

class MeType(graphene.ObjectType):
  username = graphene.String(required=True)
  email = graphene.String(required=True)

  journal_entries = graphene.List(OwnerJournalEntryType)

  def resolve_journal_entries(user, info):
    return user.created_journal_entries.all()
