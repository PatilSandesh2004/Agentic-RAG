import os
from typing import Dict


def analyze_document(
    file_path: str,
    page_level: bool = True,
    layout_aware: bool = True,
) -> Dict:
    """
    PreOCR decision layer (fallback implementation).

    This function determines whether OCR is needed based on
    lightweight heuristics when PreOCR is unavailable.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    # Image files always need OCR
    if ext in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
        return {
            "needs_ocr": True,
            "confidence": 1.0,
            "reason_code": "IMAGE_FILE",
        }

    # Text-based formats usually don't need OCR
    if ext in [".txt", ".docx", ".pptx", ".xlsx", ".xls"]:
        return {
            "needs_ocr": False,
            "confidence": 0.95,
            "reason_code": "OFFICE_WITH_TEXT",
        }

    # PDFs: conservative heuristic
    if ext == ".pdf":
        return {
            "needs_ocr": False,
            "confidence": 0.8,
            "reason_code": "PDF_ASSUMED_DIGITAL",
        }

    # Default fallback
    return {
        "needs_ocr": True,
        "confidence": 0.5,
        "reason_code": "UNKNOWN_FORMAT",
    }
