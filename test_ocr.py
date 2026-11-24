print("Starting OCR test...")

from engine.ocr_engine import extract_text

print("OCR module imported successfully!")

image_path = "samples/test_01.png"

print("Processing image:", image_path)

result = extract_text(image_path)

print("\n========== EXTRACTED TEXT ==========")

print(result["text"])

print("\n========== WORD DETAILS ==========")

for word in result["words"]:

    print("Word:", word["text"])
    print("Confidence:", word["confidence"])

    print(
        "Position:",
        word["left"],
        word["top"],
        word["width"],
        word["height"]
    )

    print("---------------------------")

print("\nOCR test completed!")