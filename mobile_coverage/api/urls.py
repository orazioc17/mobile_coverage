from django.urls import path
from . import views


urlpatterns = [
    path("coverage/", views.get_coverage, name="get_coverage"),
]
