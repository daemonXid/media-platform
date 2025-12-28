from django.db import models
from modules.base.core.models import TimestampedModel


class VisualMedia(TimestampedModel):
    """
    Represents an uploaded image or video for analysis.
    Works independently of AI features (Basic Media Viewer).
    """

    MEDIA_TYPES = [
        ("IMAGE", "Image"),
        ("VIDEO", "Video"),
    ]

    user_id = models.IntegerField(db_index=True)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="vision/uploads/%Y/%m/%d/")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default="IMAGE")

    # Source Info
    source_url = models.URLField(max_length=500, blank=True, help_text="Original YouTube/Web URL")

    # Metadata (Non-AI)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    duration_seconds = models.FloatField(default=0.0, help_text="Video duration", null=True, blank=True)
    file_size_bytes = models.BigIntegerField(default=0)

    # Analysis State
    is_analyzed = models.BooleanField(default=False)
    analysis_provider = models.CharField(max_length=50, blank=True, help_text="e.g., MediaPipe, YOLO")

    class Meta:
        db_table = "vision_visual_media"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_media_type_display()})"


class AnalysisResult(TimestampedModel):
    """
    Stores the AI analysis result (skeletons, boxes).
    Separated to allow re-analysis or multiple analysis types.
    """

    media = models.ForeignKey(VisualMedia, on_delete=models.CASCADE, related_name="analysis_results")

    # Analysis Configuration
    analysis_type = models.CharField(
        max_length=50,
        choices=[
            ("POSE", "Pose Estimation"),
            ("HAND", "Hand Tracking"),
            ("OBJECT", "Object Detection (YOLO)"),
            ("FACE", "Face Mesh"),
        ],
    )

    # The heavy data
    raw_data = models.JSONField(help_text="Standardized JSON: {frames: [{timestamp: 0, keypoints: [...]}]}")

    processing_time_ms = models.IntegerField(default=0)
    confidence_score = models.FloatField(default=0.0)

    class Meta:
        db_table = "vision_analysis_result"


class MediaComment(TimestampedModel):
    """
    Community interaction on media items.
    """

    media = models.ForeignKey(VisualMedia, on_delete=models.CASCADE, related_name="comments")
    user_id = models.IntegerField()
    content = models.TextField()

    # Optional: Timeline comment
    timestamp_seconds = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "vision_media_comment"
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user_id} on {self.media}"
