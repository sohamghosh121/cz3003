from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^healthCheck/', views.healthCheck),
    url(r'^log/', views.getTransactionLog),
    url(r'^crisis', views.getCrisisView),
    url(r'^getDistricts', views.getDistricts),
    # url(r'^setCrisis', views.setCrisis)
]
