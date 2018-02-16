from django.shortcuts import render
from django.views.generic import View

class OptOutOfEmailView(View):
  def get(self, request):
    print(request.data)
    print("Moo")
