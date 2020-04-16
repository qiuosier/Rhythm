from django.conf.urls import url

from . import views

app_name = 'covid19'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
