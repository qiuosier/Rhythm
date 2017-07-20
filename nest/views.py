from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from google.appengine.api import urlfetch
from .data.home_page import CAROUSEL_DATA, BIRDS


def index(request):
    return render(request, "nest/index.html", {
        'carousel_data': CAROUSEL_DATA,
        'birds': BIRDS,
    })


def about(request):
    return render(request, "nest/about.html", {
        
    })


def activate(request):
    try:
        r = urlfetch.fetch('http://qiu.azurewebsites.net', method='GET', deadline=20)
        if r.status_code == 200:
            return HttpResponse("Nest activated successfully.")
        else:
            return HttpResponseBadRequest("Status Code: " + str(r.status_code))
    except Exception as ex:
        return HttpResponse("Exception.")
