from django.conf.urls import include, url
from django.views.generic import RedirectView
import views


urlpatterns = [
	url(r'^$', RedirectView.as_view(url='log')),
    # url(r'^healthCheck/', views.healthCheck),
    url(r'^log/', views.get_transaction_log),
    url(r'^crisis', views.get_crisis_view),
    url(r'^get_districts', views.get_districts),
    url(r'^set_crisis', views.set_crisis),
    url(r'^map', views.map_events),
    url(r'^list', views.list_events),
    url(r'^delete_event', views.delete_event)
]
