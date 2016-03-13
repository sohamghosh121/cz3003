from django.conf.urls import include, url
from django.views.generic import RedirectView
import views


urlpatterns = [
	url(r'^$', RedirectView.as_view(url='new')),
    url(r'^healthCheck/', views.healthCheck),
    url(r'^new', views.newEvent),
    url(r'^list', views.listEvents),
    url(r'^map', views.mapEvents),
    url(r'^updateEvent', views.updateEvent),
    url(r'^deactivateEvent', views.deactivateEvent),
    url(r'^getEventUpdateForm', views.getEventUpdateForm),
]
