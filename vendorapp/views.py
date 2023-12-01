from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.


def vendorapp(request):
    return HttpResponse("Welcome to vendor management")

