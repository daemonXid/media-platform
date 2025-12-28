from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.conf import settings
from .models import ResearchPaper
from .services import MinerUService
from .selectors import list_user_papers, get_paper_by_id

service = MinerUService()


def index(request: HttpRequest) -> HttpResponse:
    """Dashboard for My Papers."""
    papers = list_user_papers(user_id=request.user.id if request.user.is_authenticated else 0)
    return render(request, "smart_paper/index.html", {"papers": papers})


def viewer(request: HttpRequest, paper_id: int) -> HttpResponse:
    """The main 'Formula-Alive' split viewer."""
    paper = get_paper_by_id(paper_id)
    return render(request, "smart_paper/viewer.html", {"paper": paper})


@require_POST
def upload_paper(request: HttpRequest) -> HttpResponse:
    """
    HTMX: Handles file upload and returns the processing row/card.
    """
    if "pdf_file" not in request.FILES:
        return HttpResponse("No file uploaded", status=400)

    file = request.FILES["pdf_file"]
    title = request.POST.get("title", file.name)

    paper = ResearchPaper.objects.create(
        user_id=request.user.id if request.user.is_authenticated else 0,
        title=title,
        original_pdf=file,
    )

    # Trigger processing
    service.process_paper(paper)

    # Return a row that will poll for status
    context = {"paper": paper}
    return render(request, "smart_paper/partials/paper_row.html", context)


def poll_status(request: HttpRequest, paper_id: int) -> HttpResponse:
    """
    HTMX: Polled by the UI to check processing status.
    Returns:
     - The same spinner/status if PROCESSING
     - The 'View' button if COMPLETED
     - Error message if FAILED
    """
    paper = get_paper_by_id(paper_id)

    if paper.processing_status == "COMPLETED":
        # Return the final state row (with View button)
        # OOB Swap could be used here to update other parts of the UI
        return render(request, "smart_paper/partials/paper_row_completed.html", {"paper": paper})
    elif paper.processing_status == "FAILED":
        return HttpResponse('<span class="text-red-500">Processing Failed</span>')
    else:
        # Keep polling (content containing hx-trigger='every 2s')
        return render(request, "smart_paper/partials/processing_status.html", {"paper": paper})


@require_http_methods(["DELETE"])
def delete_paper(request: HttpRequest, paper_id: int) -> HttpResponse:
    """Delete paper."""
    paper = get_object_or_404(ResearchPaper, id=paper_id)
    paper.delete()
    return HttpResponse("")
