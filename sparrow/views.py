from django.shortcuts import render
from django.http import HttpResponse
from .data.home_page import CAROUSEL_DATA, BIRDS


# Create your views here.
def index(request):
    return render(request, "sparrow/index.html", {
        'carousel_data': CAROUSEL_DATA,
        'birds': BIRDS,
    })
