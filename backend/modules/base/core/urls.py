"""
🌐 daemon URLs - HTMX Endpoints

This module defines URL patterns for the daemon module.
All HTMX endpoints are prefixed with /htmx/ for clarity.
"""

from django.urls import path

from . import views

app_name = "daemon"

urlpatterns = [
    # Page views
    path("", views.home, name="home"),
    path("getting-started/", views.getting_started, name="getting_started"),
    # HTMX fragment endpoints
    path("htmx/time/", views.htmx_time, name="htmx_time"),
    path("htmx/counter/", views.htmx_counter, name="htmx_counter"),
    path("htmx/search/", views.htmx_search, name="htmx_search"),
    path("htmx/toast/", views.htmx_toast, name="htmx_toast"),
]
