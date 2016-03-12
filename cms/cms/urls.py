"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin as djangoadmin
from django.conf.urls.static import static
from django.views.generic import TemplateView
import views
import settings
import operator.urls
import admin.urls

urlpatterns = [
    url(r'^djangoadmin/', include(djangoadmin.site.urls)),
    url(r'^healthCheck/', views.healthCheck),
    url(r'^operator/', include('cms.operator.urls')),
    url(r'^admin/', include('cms.admin.urls')),
    url(r'^login_view', views.loginView),
    url(r'^login/', TemplateView.as_view(template_name='login.html')),
    url(r'^getWeatherInfo', views.pullWeatherInfo),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
