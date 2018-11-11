from django.conf.urls import url

from . import views

app_name = 'nest'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Basic page rendering
    url(r'^page/(?P<filename>.*)/$', views.page, name='page'),
    url(r'^timeline/(?P<filename>.*)/$', views.timeline, name='timeline'),
    url(r'^skylark/(?P<collection>.*)/$', views.skylark_collection, name='skylark_collection'),
    
    # The following patterns all use the "load_data_and_render" view (nest:rhythm).
    url(
        r'^render/(?P<html_name>.*?)/data/(?P<json_name>.*?)/trasnform/(?P<transform_name>.*?)$', 
        views.load_data_and_render, 
        name='rhythm'
    ),
    url(r'^render/(?P<html_name>.*?)/data/(?P<json_name>.*?)/$', views.load_data_and_render, name='rhythm'),
    url(r'^render/(?P<html_name>.*?)/$', views.load_data_and_render, name='rhythm'),
    # If none of the above matches, try to load html/json and render a template
    url(r'^(?P<html_name>.*)/$', views.load_data_and_render, name='rhythm'),
]