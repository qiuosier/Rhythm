from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from google.appengine.api import urlfetch


def index(request):
    return HttpResponse("Hello, world. You're at the nest app index with app engine standard environment.")


def activate(request):
    try:
        r = urlfetch.fetch('http://qiu.azurewebsites.net', method='GET', deadline=20)
        if r.status_code == 200:
            return HttpResponse("Nest activated successfully.")
        else:
            return HttpResponseBadRequest("Status Code: " + str(r.status_code))
    except Exception as ex:
        return HttpResponse("Exception.")
