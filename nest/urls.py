from django.conf.urls import url

from . import views

app_name = 'nest'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rhythm/(?P<file_name>.*)/$', views.load_data_and_render, name='rhythm'),
    url(r'^activate/$', views.activate, name='activate')
]