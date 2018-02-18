from . import views

from django.conf.urls import url

urlpatterns = [
  url(r"^opt-out", views.OptOutView.as_view(), name="mail_opt_out"),
]
