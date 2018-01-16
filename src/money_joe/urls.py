from graphql_api.schema import schema

from django.conf.urls import url
from django.contrib import admin
from graphene_django.views import GraphQLView

urlpatterns = [
  url(r"^graphql$", GraphQLView.as_view(graphiql=True, schema=schema)),
  url(r"^admin/", admin.site.urls),
]
