"""rhythm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from Aries.storage import LocalFolder

urlpatterns = [
    url(r'^robots.txt$', 
    lambda r: HttpResponse("User-agent: *\nAllow: /\n", 
    content_type = "text/plain")),
]

# Add URLs of apps.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_folders = LocalFolder(BASE_DIR).folders
for folder in root_folders:
    if "urls.py" in folder.file_names and folder.name not in ['nest', 'rhythm']:
        urlpatterns.append(
            url(r'^%s/' % str(folder.name).lower(), include('%s.urls' % folder.name)),
        )

urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('nest.urls')),
]
