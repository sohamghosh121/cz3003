from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^healthCheck/', views.healthCheck),
    url(r'^new', views.newEvent),
    url(r'^list', views.listEvents),
    url(r'^map', views.mapEvents),
    url(r'^getEventsGeoJSON', views.getEventsGeoJSON)
]
