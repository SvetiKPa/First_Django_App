from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def hello_world(request, user_name):
    return HttpResponse(f"<h1>Hello, {user_name} in DJANGO! </h1>")