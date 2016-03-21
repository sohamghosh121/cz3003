from django.conf.urls import include, url
from cms.report import views

urlpatterns = [
    url(r'^get_traffic_info', views.get_traffic_info),
    url(r'^get_terrorist_info', views.get_terrorist_info),
    url(r'^get_map_image', views.get_map_image),
    url(r'^get_crisis_info', views.get_crisis_info)
]