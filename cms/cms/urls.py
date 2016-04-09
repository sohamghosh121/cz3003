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
from django.views.generic import TemplateView, RedirectView
import views
import settings
import operator.urls
import admin.urls
import report.urls

urlpatterns = [
    url(r'^djangoadmin/', include(djangoadmin.site.urls)),
    # url(r'^healthCheck/', views.healthCheck),
    url(r'^operator/', include('cms.operator.urls')),
    url(r'^admin/', include('cms.admin.urls')),
    url(r'^report/', include('cms.report.urls')),
    url(r'^public/', include('cms.public.urls')),
    url(r'^login_view', views.login_view),
    url(r'^login', TemplateView.as_view(template_name='login.html')),
    url(r'^logout', views.logout_view),
    url(r'^index', TemplateView.as_view(template_name='index.html')),
    url(r'^report/', TemplateView.as_view(template_name='report.html')),
    url(r'^get_weather_info', views.get_weather_info),
    url(r'^get_dengue_info', views.get_dengue_info),
    url(r'^refreshAPI', views.refreshAPI),
    url(r'^get_district_info', views.get_district_info),
    url(r'^get_events_geo_JSON', views.get_events_geo_JSON),
    url(r'^maps/weather', TemplateView.as_view(template_name='maps/weather.html')),
    url(r'^maps/dengue', TemplateView.as_view(template_name='maps/dengue.html')),
    url(r'^maps/terrorist', TemplateView.as_view(template_name='maps/terrorist.html')),
    url(r'^maps/traffic', TemplateView.as_view(template_name='maps/traffic.html')),
    url(r'^maps/crisis', TemplateView.as_view(template_name='maps/crisis.html')),
    url(r'^$', RedirectView.as_view(url='public'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
