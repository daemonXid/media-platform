from ninja import Schema, ModelSchema
from typing import List, Optional, Dict, Any
from .models import ResearchPaper, FormulaSnippet, PaperAnnotation


class PaperUploadSchema(Schema):
    title: str


class FormulaSchema(ModelSchema):
    class Meta:
        model = FormulaSnippet
        fields = [
            "id",
            "latex_original",
            "python_expression",
            "variables_metadata",
            "description",
            "location_index",
        ]


class AnnotationSchema(ModelSchema):
    class Meta:
        model = PaperAnnotation
        fields = [
            "id",
            "user_id",
            "target_text",
            "position_selector",
            "content",
            "created_at",
        ]


class PaperDetailSchema(ModelSchema):
    formulas: List[FormulaSchema]
    recent_annotations: List[AnnotationSchema] = []

    class Meta:
        model = ResearchPaper
        fields = [
            "id",
            "title",
            "processing_status",
            "extracted_markdown",
            "created_at",
        ]

    @staticmethod
    def resolve_recent_annotations(obj):
        return obj.annotations.all().order_by("-created_at")[:5]
