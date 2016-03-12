from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'^healthCheck/', views.healthCheck),
]
