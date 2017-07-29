from django.conf.urls import url

from . import views

app_name = 'authentication'
urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout')
]