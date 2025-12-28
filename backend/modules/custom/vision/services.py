import cv2
import json
import logging
from pathlib import Path
import numpy as np
from django.conf import settings
from .models import VisualMedia, AnalysisResult

logger = logging.getLogger(__name__)


class VisionService:
    """
    Handles media processing.
    Designing for 'Graceful Degradation' - checks for library availability.
    """

    def __init__(self):
        # Check for AI libraries
        self.mediapipe_available = False
        try:
            import mediapipe as mp

            self.mp = mp
            self.mediapipe_available = True
        except ImportError:
            logger.warning("MediaPipe not installed. AI features disabled.")

        # Check for yt-dlp
        self.ytdlp_available = False
        try:
            import yt_dlp

            self.ytdlp = yt_dlp
            self.ytdlp_available = True
        except ImportError:
            logger.warning("yt-dlp not installed. YouTube download disabled.")

    def download_youtube_video(self, url: str, user_id: int) -> VisualMedia:
        """
        Downloads a video from YouTube using yt-dlp.
        Returns a VisualMedia object.
        """
        if not self.ytdlp_available:
            raise ImportError("yt-dlp is not installed.")

        try:
            # Output template
            out_dir = Path(settings.MEDIA_ROOT) / "vision" / "downloads"
            out_dir.mkdir(parents=True, exist_ok=True)
            out_template = str(out_dir / "%(id)s.%(ext)s")

            ydl_opts = {
                "outtmpl": out_template,
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",  # Ensure MP4 for web compatibility
                "noplaylist": True,
            }

            with self.ytdlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                # Relative path for Django FileField
                rel_path = Path("vision") / "downloads" / Path(filename).name

                # Create Media Object
                media = VisualMedia.objects.create(
                    user_id=user_id,
                    title=info.get("title", "YouTube Video"),
                    file=str(rel_path),
                    media_type="VIDEO",
                    source_url=url,
                    duration_seconds=info.get("duration", 0),
                    width=info.get("width", 0),
                    height=info.get("height", 0),
                )

                # If width/height missing from info, run extract_metadata
                if media.width == 0:
                    self.extract_metadata(media)

                return media

        except Exception as e:
            logger.error(f"YouTube download failed: {e}")
            raise e

    def extract_metadata(self, media: VisualMedia):
        """
        Extracts execution-independent metadata (Basic Viewer Mode).
        Uses OpenCV for basic properties.
        """
        try:
            path = media.file.path
            cap = cv2.VideoCapture(path)

            if not cap.isOpened():
                return

            media.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            media.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            media.file_size_bytes = Path(path).stat().st_size

            if media.media_type == "VIDEO":
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                if fps > 0:
                    media.duration_seconds = frame_count / fps

            media.save()
            cap.release()
        except Exception as e:
            logger.error(f"Metadata extraction failed: {e}")

    def run_pose_estimation(self, media: VisualMedia) -> bool:
        """
        Runs MediaPipe Pose on the media.
        """
        if not self.mediapipe_available:
            logger.error("MediaPipe currently unavailable.")
            return False

        try:
            mp_pose = self.mp.solutions.pose

            # Using context manager for resources
            with mp_pose.Pose(
                static_image_mode=(media.media_type == "IMAGE"),
                model_complexity=2,
                enable_segmentation=True,
                min_detection_confidence=0.5,
            ) as pose:
                results_data = {"frames": []}

                cap = cv2.VideoCapture(media.file.path)
                frame_idx = 0

                while cap.isOpened():
                    success, image = cap.read()
                    if not success:
                        break

                    # Convert BGR to RGB
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = pose.process(image_rgb)

                    frame_data = {
                        "frame_index": frame_idx,
                        "timestamp": cap.get(cv2.CAP_PROP_POS_MSEC),
                        "landmarks": [],
                    }

                    if results.pose_landmarks:
                        for landmark in results.pose_landmarks.landmark:
                            frame_data["landmarks"].append(
                                {
                                    "x": landmark.x,
                                    "y": landmark.y,
                                    "z": landmark.z,
                                    "visibility": landmark.visibility,
                                }
                            )

                    results_data["frames"].append(frame_data)
                    frame_idx += 1

                    if media.media_type == "IMAGE":
                        break

                cap.release()

                # Save Result
                AnalysisResult.objects.create(
                    media=media,
                    analysis_type="POSE",
                    raw_data=results_data,
                    confidence_score=0.9,  # Mock
                )

                media.is_analyzed = True
                media.save()
                return True

        except Exception as e:
            logger.error(f"Pose estimation failed: {e}", exc_info=True)
            return False
