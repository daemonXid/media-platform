import os

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def manual_home(request: HttpRequest) -> HttpResponse:
    """Manual home page listing all modules."""
    modules_base = os.listdir(os.path.join(settings.BASE_DIR, "backend/modules/base"))
    modules_ai = os.listdir(os.path.join(settings.BASE_DIR, "backend/modules/ai"))
    modules_custom = os.listdir(os.path.join(settings.BASE_DIR, "backend/modules/custom"))

    return render(
        request,
        "manual/home.html",
        {
            "base": sorted([m for m in modules_base if not m.startswith("_")]),
            "ai": sorted([m for m in modules_ai if not m.startswith("_")]),
            "custom": sorted([m for m in modules_custom if not m.startswith("_")]),
        },
    )
