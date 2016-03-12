from django.conf.urls import include, url
from cms.report import views

urlpatterns = [
    url(r'^getTrafficInfo', views.getTrafficInfo),
    url(r'^getTerroristInfo', views.getTerroristInfo)
]