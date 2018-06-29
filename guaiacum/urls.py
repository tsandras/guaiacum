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
from django.conf.urls.static import static
from django.conf import settings

from editor import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^editor_new/', views.editor_new, name='editor_new'),
    url(r'^editor/(?P<character_id>\d+)/$', views.editor, name='editor'),
    url(r'^page/(?P<page_id>\d+)/$', views.page, name='page'),
    url(r'^pages/$', views.pages, name='pages'),
    url(r'^home/', views.home, name='home'),
    url(r'^attributes_phy/', views.attributes_phy, name='attributes_con'),
    url(r'^attributes_con/', views.attributes_con, name='attributes_phy'),
    url(r'^attributes_men/', views.attributes_men, name='attributes_men'),
    url(r'^attributes_com/', views.attributes_com, name='attributes_com'),
    url(r'^attributes_mag/', views.attributes_mag, name='attributes_mag'),
    url(r'^attributes_his/', views.attributes_his, name='attributes_his'),
    url(r'^advantages/', views.advantages, name='advantages'),
    url(r'^attributes/', views.attributes, name='attributes'),
    url(r'^advantage/(?P<advantage_id>\d+)/$', views.advantage, name='advantage'),
    url(r'^attribute/(?P<attribute_id>\d+)/$', views.attribute, name='attribute'),
    url(r'^save_character/', views.save_character, name='save_character'),
    url(r'^delete_advantage/', views.delete_advantage, name='delete_advantage'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$',  TemplateView.as_view(template_name="about.html")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
