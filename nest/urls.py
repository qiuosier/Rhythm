from django.conf.urls import url

from . import views

app_name = 'nest'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^skylark/(?P<collection>.*)/$', views.skylark_collection, name='skylark_collection'),
    url(r'^rhythm/(?P<json_name>.*)/$', views.load_data_and_render, name='rhythm'),
    url(r'^page/(?P<filename>.*)/$', views.page, name='page'),
    url(r'^cards/(?P<filename>.*)/$', views.cards, name='cards'),
    url(r'^timeline/(?P<filename>.*)/$', views.timeline, name='timeline'),
    url(r'^activate/$', views.activate, name='activate')
]