"""jdr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic import TemplateView

from editor import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^editor_new/', views.editor_new, name='editor_new'),
    url(r'^editor/(?P<character_id>\d+)/$', views.editor, name='editor'),
    url(r'^home/', views.home, name='home'),
    url(r'^advantages/', views.advantages, name='advantages'),
    url(r'^advantage/(?P<advantage_id>\d+)/$', views.advantage, name='advantage'),
    url(r'^save_character/', views.save_character, name='save_character'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$',  TemplateView.as_view(template_name="about.html")),
]
