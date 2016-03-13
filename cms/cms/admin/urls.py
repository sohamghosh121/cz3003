from django.conf.urls import include, url
from django.views.generic import RedirectView
import views


urlpatterns = [
	url(r'^$', RedirectView.as_view(url='log')),
    url(r'^healthCheck/', views.healthCheck),
    url(r'^log/', views.getTransactionLog),
    url(r'^crisis', views.getCrisisView),
    url(r'^getDistricts', views.getDistricts),
    url(r'^setCrisis', views.setCrisis),
    url(r'^map', views.mapEvents),
    url(r'^list', views.listEvents),
    url(r'^deleteEvent', views.deleteEvent)
]
