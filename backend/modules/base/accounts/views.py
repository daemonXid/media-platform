"""
🌐 Auth Views

Custom views for user profile.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """User profile page acting as a Dashboard."""
    # Lazy import to avoid circular dependency/architectural strictness for now
    from modules.custom.vision.models import VisualMedia, MediaComment
    from modules.custom.smart_paper.models import ResearchPaper

    # Vision Data
    media_list = VisualMedia.objects.filter(user_id=request.user.id).order_by("-created_at")
    media_comments = (
        MediaComment.objects.filter(user_id=request.user.id).select_related("media").order_by("-created_at")
    )

    # Smart Paper Data
    papers = ResearchPaper.objects.filter(user_id=request.user.id).order_by("-created_at")

    # Context
    context = {
        "media_list": media_list,
        "media_comments": media_comments,
        "papers": papers,
        # "paper_comments": ... (To be added)
    }

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update_image" and request.FILES.get("profile_image"):
            request.user.profile_image = request.FILES["profile_image"]
            request.user.save(update_fields=["profile_image"])
            return redirect("auth:profile")

    return render(request, "account/profile.html", context)
