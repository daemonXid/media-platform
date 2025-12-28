from django.db import models
from modules.base.core.models import TimestampedModel


class ResearchPaper(TimestampedModel):
    """
    Represents a scientific paper uploaded for analysis.
    """

    user_id = models.IntegerField(db_index=True)
    title = models.CharField(max_length=255, blank=True)
    original_pdf = models.FileField(upload_to="research/papers/%Y/%m/%d/")

    # MinerU processing status
    processing_status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("PROCESSING", "Processing"),
            ("COMPLETED", "Completed"),
            ("FAILED", "Failed"),
        ],
        default="PENDING",
    )

    # The full extracted markdown content
    extracted_markdown = models.TextField(blank=True)

    # Metadata
    page_count = models.IntegerField(default=0)
    input_tokens = models.IntegerField(default=0)  # For cost tracking if using LLM

    class Meta:
        db_table = "research_smart_paper"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Paper #{self.id}"


class FormulaSnippet(TimestampedModel):
    """
    An interactive formula extracted from a paper.
    Enabled for 'Formula-Alive Viewer' feature.
    """

    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, related_name="formulas")

    # The raw LaTeX captured from OCR/MinerU
    latex_original = models.TextField()

    # Converted executable format (for Python eval or JS calc)
    python_expression = models.TextField(blank=True, help_text="Executable Python code for this formula")

    # Variable definitions for UI generation (e.g. Mass (kg), Velocity (m/s))
    variables_metadata = models.JSONField(default=dict, help_text="Schema for variables: name, unit, default_value")

    description = models.TextField(blank=True)
    location_index = models.IntegerField(default=0, help_text="Position ordering in the document")

    class Meta:
        db_table = "research_formula_snippet"
        ordering = ["location_index"]


class PaperAnnotation(TimestampedModel):
    """
    Collaborative annotations on the paper.
    Enables 'Contextual Annotation' feature.
    """

    paper = models.ForeignKey(ResearchPaper, on_delete=models.CASCADE, related_name="annotations")
    user_id = models.IntegerField()

    # Semantic location
    target_text = models.TextField(blank=True)  # The text being highlighted
    position_selector = models.JSONField(default=dict, help_text="PDF coordination or DOM selector")

    content = models.TextField()

    class Meta:
        db_table = "research_paper_annotation"
        ordering = ["created_at"]
