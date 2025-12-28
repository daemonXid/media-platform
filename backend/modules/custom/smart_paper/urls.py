from django.urls import path
from . import views

app_name = "smart_paper"

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload_paper, name="upload"),
    path("viewer/<int:paper_id>/", views.viewer, name="viewer"),
    path("status/<int:paper_id>/", views.poll_status, name="poll_status"),
    path("delete/<int:paper_id>/", views.delete_paper, name="delete_paper"),
]
