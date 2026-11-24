
from pathlib import Path

from engine.image_preprocessor import preprocess_image
from engine.ocr_engine import extract_text


def run_ocr_pipeline(image_path, language="eng"):

    image_path = Path(image_path)

    # Step 1: Preprocess image
    processed_image = preprocess_image(image_path)

    # Step 2: Extract text using OCR
    ocr_results = extract_text(
        processed_image,
        language=language
    )

    # Step 3: Return complete results
    return {
        "original_image": str(image_path),
        "processed_image": str(processed_image),
        "extracted_text": ocr_results["text"],
        "words": ocr_results["words"],
        "lines": ocr_results["lines"],
        "paragraphs": ocr_results["paragraphs"]
    }
