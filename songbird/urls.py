from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='songbird-index'),
    url(r'^timeline/$', views.timeline, name='timeline')
]