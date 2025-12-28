import re
import logging
from pathlib import Path
from django.conf import settings
from .models import ResearchPaper, FormulaSnippet

logger = logging.getLogger(__name__)


class MinerUService:
    """
    Service to handle PDF processing using MinerU (magic-pdf).
    """

    def process_paper(self, paper: ResearchPaper) -> bool:
        """
        Executes the MinerU pipeline for a given paper.
        Returns True if successful.
        """
        paper.processing_status = "PROCESSING"
        paper.save(update_fields=["processing_status"])

        try:
            # Locate the file
            if not paper.original_pdf:
                raise ValueError("No PDF file attached to paper.")

            pdf_path = Path(paper.original_pdf.path)
            output_dir = (
                Path(settings.MEDIA_ROOT) / "research" / "processed" / str(paper.id)
            )
            output_dir.mkdir(parents=True, exist_ok=True)

            logger.info(f"Starting MinerU processing for {pdf_path}...")

            # ---------------------------------------------------------
            # [Step 1] Execute MinerU (magic-pdf)
            # ---------------------------------------------------------
            # Command: magic-pdf -p input.pdf -o output_dir
            # Note: Ensure 'magic-pdf' is installed in the environment (pip install magic-pdf)
            # cmd = ["magic-pdf", "-p", str(pdf_path), "-o", str(output_dir)]
            # subprocess.run(cmd, check=True, capture_output=True)

            # [MOCK IMPLEMENTATION]
            # Since we can't guarantee the binary is present in this agent encironment,
            # we simulate the output for the 'Vertical Slice' demonstration.

            mock_markdown = f"""
# Analysis of {paper.title}

## Abstract
This paper explores the biomechanics of high-velocity pitching.

## Methodology
The force is calculated as:
$$ F = m \times a $$

Where:
- $m$ is mass (kg)
- $a$ is acceleration (m/s^2)

## Results
We observed a significant increase in VO2Max.
            """
            paper.extracted_markdown = mock_markdown

            # ---------------------------------------------------------
            # [Step 2] Post-Processing (Formula Extraction)
            # ---------------------------------------------------------
            self._extract_formulas(paper, mock_markdown)

            paper.processing_status = "COMPLETED"
            paper.save(update_fields=["processing_status", "extracted_markdown"])
            return True

        except Exception as e:
            logger.error(f"MinerU processing failed: {e}", exc_info=True)
            paper.processing_status = "FAILED"
            paper.save(update_fields=["processing_status"])
            return False

    def _extract_formulas(self, paper: ResearchPaper, markdown_text: str):
        """
        Parses Markdown to identify LaTeX blocks and save them as FormulaSnippets.
        """
        # Rewrite to find block formulas $$ ... $$
        # This is a naive regex for demonstration.
        block_pattern = r"\$\$(.*?)\$\$"
        matches = re.findall(block_pattern, markdown_text, re.DOTALL)

        for idx, latex in enumerate(matches):
            FormulaSnippet.objects.create(
                paper=paper,
                latex_original=latex.strip(),
                location_index=idx,
                description=f"Formula #{idx + 1} extracted from text.",
            )

        # TODO: Enhanced logic to parse variables from surrounding text using LLM

    def translate_paper(self, paper: ResearchPaper, target_lang: str = "ko") -> str:
        """
        Translates the paper's markdown content while preserving LaTeX formulas.
        This enables the 'Cross-Border Insight' feature.
        """
        if not paper.extracted_markdown:
            return ""

        logger.info(f"Translating paper {paper.id} to {target_lang}")

        # [MOCK IMPLEMENTATION]
        # In a real implementation, this would:
        # 1. Regex replace $$...$$ with placeholders [FORMULA_1]
        # 2. Send text to LLM (DeepSeek/GPT-4) with prompt "Translate to Korean, keep placeholders"
        # 3. Restore placeholders

        translated_text = f"""
# {paper.title} (번역됨)

## 요약
이 논문은 고속 투구의 생체 역학을 탐구합니다.

## 방법론
힘은 다음과 같이 계산됩니다:
$$ F = m \\times a $$

여기서:
- $m$ 은 질량 (kg) 입니다.
- $a$ 는 가속도 (m/s^2) 입니다.

## 결과
우리는 VO2Max의 유의미한 증가를 관찰했습니다.
        """
        return translated_text
