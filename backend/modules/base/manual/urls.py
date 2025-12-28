from django.urls import path

from . import views

app_name = "manual"

urlpatterns = [
    path("docs/", views.manual_home, name="home"),
]
