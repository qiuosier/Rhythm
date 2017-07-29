from django.conf.urls import url

from . import views

app_name = 'songbird'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^timeline/$', views.timeline, name='timeline')
]