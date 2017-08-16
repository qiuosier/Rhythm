from django.conf.urls import url

from . import views

app_name = 'nest'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rhythm/(?P<json_name>.*)/$', views.load_data_and_render, name='rhythm'),
    url(r'^paper/(?P<filename>.*)/$', views.paper, name='paper'),
    url(r'^cards/(?P<filename>.*)/$', views.cards, name='cards'),
    url(r'^timeline/(?P<filename>.*)/$', views.timeline, name='timeline'),
    url(r'^activate/$', views.activate, name='activate')
]