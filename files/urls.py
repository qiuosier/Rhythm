from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

app_name = 'files'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload, name='upload'),
]
