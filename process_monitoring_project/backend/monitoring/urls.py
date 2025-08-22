from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("api/hosts/", views.hosts),
    path("api/processes/latest/", views.latest),
    path("api/processes/ingest/", views.ingest),
]
