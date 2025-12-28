"""
🌐 Chatbot Views

HTMX views for the chat interface.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .interface import ask_question, index_project, search_project


def chat_page(request: HttpRequest) -> HttpResponse:
    """Main chat page."""
    # Ensure project is indexed
    index_project()

    return render(request, "chatbot/chat.html")


@require_http_methods(["POST"])
def send_message(request: HttpRequest) -> HttpResponse:
    """
    Handle chat message submission.
    Returns HTMX fragment with response.
    """
    question = request.POST.get("question", "").strip()

    if not question:
        return render(
            request,
            "chatbot/_message.html",
            {"role": "assistant", "content": "질문을 입력해주세요."},
        )

    # Get AI response
    response = ask_question(question)

    return render(
        request,
        "chatbot/_message.html",
        {
            "role": "assistant",
            "question": question,
            "content": response.answer,
            "sources": response.sources,
        },
    )


@require_http_methods(["POST"])
def search(request: HttpRequest) -> HttpResponse:
    """
    Search project files.
    Returns HTMX fragment with results.
    """
    query = request.POST.get("query", "").strip()

    if not query:
        return HttpResponse("")

    results = search_project(query)

    return render(
        request,
        "chatbot/_search_results.html",
        {"results": results},
    )
