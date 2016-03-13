from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^healthCheck/', views.healthCheck),
    url(r'^new', views.newEvent),
    url(r'^list', views.listEvents),
    url(r'^map', views.mapEvents),
    url(r'^updateEvent', views.updateEvent),
    url(r'^deactivateEvent', views.deactivateEvent),
    url(r'^getEventsGeoJSON', views.getEventsGeoJSON),
    url(r'^getEventUpdateForm', views.getEventUpdateForm),
    url(r'^refreshAPI', views.refreshAPI)
]
