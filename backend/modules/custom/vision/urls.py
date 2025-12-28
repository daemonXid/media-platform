from django.urls import path
from . import views

app_name = "vision"

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload_media, name="upload"),
    path("upload/youtube/", views.upload_youtube, name="upload_youtube"),
    path("viewer/<int:media_id>/", views.viewer, name="viewer"),
    path("analyze/<int:media_id>/", views.run_analysis, name="run_analysis"),
    path("api/data/<int:result_id>/", views.get_analysis_data, name="get_data"),
    path("comment/<int:media_id>/", views.add_comment, name="add_comment"),
    path("delete/<int:media_id>/", views.delete_media, name="delete_media"),
    path("comment/delete/<int:comment_id>/", views.delete_media_comment, name="delete_media_comment"),
]
