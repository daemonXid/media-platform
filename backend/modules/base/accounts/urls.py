"""
🔗 Auth URL Patterns
"""

from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
]
