from django.conf.urls import include, url
from django.views.generic import RedirectView
import views

urlpatterns = [
	url(r'^$', RedirectView.as_view(url='map')),
    # url(r'^healthCheck/', views.healthCheck),
    url(r'^map', views.map_events)
]
