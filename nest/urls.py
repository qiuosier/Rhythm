from django.conf.urls import url

from . import views

app_name = 'nest'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^exception/$', views.view_exception, name='view_exception'),
    # Basic page rendering
    url(r'^page/(?P<filename>.*?)/$', views.page, name='page'),
    # Customized rendering
    url(r'^skylark/(?P<collection>[^/]+?)/$', views.skylark_collection, name='skylark_collection'),
    url(r'^skylark/(?P<collection>[^/]+?)/(?P<title>.+?)/$', views.skylark_image, name='skylark_image'),
    url(r'^swan/journeys/(?P<start>[0-9]+)/(?P<size>[0-9]+)/$', views.swan_journeys, name='swan_journeys'),
    # The following patterns all use the "render_template" view (nest:render_template).
    url(
        r'^render/(?P<html_name>.*?)/data/(?P<json_name>.*?)/transform/(?P<transform_name>.*?)/$', 
        views.render_template, 
        name='render_template'
    ),
    url(r'^render/(?P<html_name>.*?)/data/(?P<json_name>.*?)/$', views.render_template, name='render_template'),
    url(r'^render/(?P<html_name>.*?)/$', views.render_template, name='render_template'),
    # If none of the above matches, try to load html/json and render a template
    url(r'^(?P<html_name>.*?)/$', views.render_template, name='render_template'),
]