from django.conf.urls import url

from . import views

app_name = 'nest'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Basic page rendering
    url(r'^page/(?P<filename>.*)/$', views.page, name='page'),
    url(r'^timeline/(?P<filename>.*)/$', views.timeline, name='timeline'),
    url(r'^skylark/(?P<collection>.*)/$', views.skylark_collection, name='skylark_collection'),
    
    # The following patterns all use the "render_template" view (nest:render_template).
    url(
        r'^render/(?P<html_name>.*?)/data/(?P<json_name>.*?)/trasnform/(?P<transform_name>.*?)$', 
        views.render_template, 
        name='render_template'
    ),
    url(r'^render/(?P<html_name>.*?)/data/(?P<json_name>.*?)/$', views.render_template, name='render_template'),
    url(r'^render/(?P<html_name>.*?)/$', views.render_template, name='render_template'),
    # If none of the above matches, try to load html/json and render a template
    url(r'^(?P<html_name>.*)/$', views.render_template, name='render_template'),
]