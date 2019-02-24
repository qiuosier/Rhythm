from django.conf.urls import url

from . import views

app_name = 'aquarius'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^azure_authenticated/$', views.index, name='azure_authenticated'),
]