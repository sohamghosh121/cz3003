from django.conf.urls import include, url
from django.views.generic import RedirectView
import views


urlpatterns = [
	url(r'^$', RedirectView.as_view(url='new')),
    # url(r'^healthCheck/', views.healthCheck),
    url(r'^new', views.new_event),
    url(r'^list', views.list_events),
    url(r'^map', views.map_events),
    url(r'^update_event', views.update_event),
    url(r'^deactivate_event', views.deactivate_event),
    url(r'^get_event_update_form', views.get_event_update_form),
]
