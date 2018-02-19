from . import views

from django.conf.urls import url

urlpatterns = [
  url(
    r"^activate$", views.ActivateAccountView.as_view(),
    name="registration_activate_account"
  ),
]
