from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from .models import VisualMedia, AnalysisResult, MediaComment
from .services import VisionService

service = VisionService()


def index(request: HttpRequest) -> HttpResponse:
    """Gallery of visual media."""
    media_list = VisualMedia.objects.filter(user_id=request.user.id if request.user.is_authenticated else 0)
    return render(request, "vision/index.html", {"media_list": media_list})


def viewer(request: HttpRequest, media_id: int) -> HttpResponse:
    """
    Dual-Mode Viewer.
    - If not analyzed: Shows simple File Viewer.
    - If analyzed: Shows Canvas Overlay + Toggle.
    """
    media = get_object_or_404(VisualMedia, id=media_id)
    latest_result = media.analysis_results.last()

    context = {
        "media": media,
        "result": latest_result,
        "ai_enabled": service.mediapipe_available,
        "comments": media.comments.all(),
    }
    return render(request, "vision/viewer.html", context)


@require_POST
def upload_media(request: HttpRequest) -> HttpResponse:
    if "media_file" not in request.FILES:
        return HttpResponse("No file", status=400)

    file = request.FILES["media_file"]
    media_type = "VIDEO" if "video" in file.content_type else "IMAGE"

    media = VisualMedia.objects.create(
        user_id=request.user.id if request.user.is_authenticated else 0,
        title=file.name,
        file=file,
        media_type=media_type,
    )

    # Run basic metadata extraction (Fast, No AI)
    service.extract_metadata(media)

    # Return row
    # Return row
    return render(request, "vision/partials/media_card.html", {"media": media})


@require_POST
def upload_youtube(request: HttpRequest) -> HttpResponse:
    """Download video from YouTube URL."""
    url = request.POST.get("youtube_url")
    if not url:
        return HttpResponse("No URL provided", status=400)

    try:
        media = service.download_youtube_video(url, request.user.id if request.user.is_authenticated else 0)
        return render(request, "vision/partials/media_card.html", {"media": media})
    except Exception as e:
        return HttpResponse(f"Download Failed: {str(e)}", status=500)


@require_POST
def run_analysis(request: HttpRequest, media_id: int) -> HttpResponse:
    """Trigger AI Analysis."""
    media = get_object_or_404(VisualMedia, id=media_id)
    analysis_type = request.POST.get("analysis_type", "POSE")

    if analysis_type == "POSE":
        success = service.run_pose_estimation(media)

    if success:
        return redirect("vision:viewer", media_id=media.id)
    else:
        return HttpResponse("Analysis Failed or AI Unavailable", status=500)


def get_analysis_data(request: HttpRequest, result_id: int) -> JsonResponse:
    """API for JS to fetch keypoints."""
    result = get_object_or_404(AnalysisResult, id=result_id)
    return JsonResponse(result.raw_data)


@require_POST
def add_comment(request: HttpRequest, media_id: int) -> HttpResponse:
    """Add a comment to the media."""
    media = get_object_or_404(VisualMedia, id=media_id)
    content = request.POST.get("comment", "").strip()

    if not content:
        return HttpResponse("Comment cannot be empty", status=400)

    comment = MediaComment.objects.create(
        media=media, user_id=request.user.id if request.user.is_authenticated else 0, content=content
    )

    return render(request, "vision/partials/comment_row.html", {"comment": comment})


@require_http_methods(["DELETE"])
def delete_media(request: HttpRequest, media_id: int) -> HttpResponse:
    """Delete media item."""
    media = get_object_or_404(VisualMedia, id=media_id)

    # Optional: Check ownership
    # if media.user_id != request.user.id: ...

    media.delete()
    return HttpResponse("")  # Return empty to remove element per HTMX


@require_http_methods(["DELETE"])
def delete_media_comment(request: HttpRequest, comment_id: int) -> HttpResponse:
    """Delete a comment."""
    comment = get_object_or_404(MediaComment, id=comment_id)
    comment.delete()
    return HttpResponse("")
