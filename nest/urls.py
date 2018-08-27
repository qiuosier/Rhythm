from django.conf.urls import url

from . import views

app_name = 'nest'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Basic page rendering
    url(r'^page/(?P<filename>.*)/$', views.page, name='page'),
    url(r'^timeline/(?P<filename>.*)/$', views.timeline, name='timeline'),
    url(r'^skylark/(?P<collection>.*)/$', views.skylark_collection, name='skylark_collection'),
    # If none of the above matches, try to load json and render a template
    url(r'^(?P<json_name>.*)/$', views.load_data_and_render, name='rhythm'),
]