from typing import List, Optional
from django.shortcuts import get_object_or_404
from .models import ResearchPaper


def list_user_papers(user_id: int) -> List[ResearchPaper]:
    """Returns all papers owned by the user."""
    return ResearchPaper.objects.filter(user_id=user_id)


def get_paper_by_id(paper_id: int) -> ResearchPaper:
    """Returns a single paper or raises 404."""
    return get_object_or_404(ResearchPaper, id=paper_id)
