from src.ingestion.preocr import analyze_document


def preocr_tool(file_path: str):
    """
    Check whether a document needs OCR.
    """
    return analyze_document(file_path)
