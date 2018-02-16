from . import views

from django.conf.urls import url

urlpatterns = [
  url(r"^opt-out-of-email", views.OptOutOfEmailView.as_view()),
]
