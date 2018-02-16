from graphql_api.schema import schema

from django.conf.urls import url, include
from django.contrib import admin
from graphene_django.views import GraphQLView

urlpatterns = [
  url(r"^user_profile/", include("user_profile.urls")),

  url(r"^graphql$", GraphQLView.as_view(graphiql=True, schema=schema)),
  url(r"^admin/", admin.site.urls),
]
