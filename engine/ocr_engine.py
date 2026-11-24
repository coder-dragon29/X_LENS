
from pathlib import Path
import pytesseract

from PIL import Image
from pytesseract import Output


def extract_text(image_path, language="eng"):

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError("Image does not exist")

    with Image.open(image_path) as image:

        results = pytesseract.image_to_data(
            image,
            lang=language,
            config="--psm 3",
            output_type=Output.DICT
        )

    words = []
    lines = {}
    paragraphs = {}

    for i in range(len(results["text"])):

        word = results["text"][i].strip()

        if not word:
            continue

        confidence = float(results["conf"][i])

        if confidence < 0:
            continue

        block_num = results["block_num"][i]
        par_num = results["par_num"][i]
        line_num = results["line_num"][i]

        word_info = {
            "text": word,
            "confidence": confidence,
            "left": results["left"][i],
            "top": results["top"][i],
            "width": results["width"][i],
            "height": results["height"][i],
            "block_num": block_num,
            "par_num": par_num,
            "line_num": line_num,
            "word_num": results["word_num"][i]
        }

        words.append(word_info)

        # Group words into lines
        line_key = (block_num, par_num, line_num)

        if line_key not in lines:
            lines[line_key] = []

        lines[line_key].append(word_info)

        # Group lines into paragraphs
        paragraph_key = (block_num, par_num)

        if paragraph_key not in paragraphs:
            paragraphs[paragraph_key] = []

        paragraphs[paragraph_key].append(word_info)

    # Reconstruct complete lines
    reconstructed_lines = []

    for key, line_words in lines.items():

        line_text = " ".join(
            word["text"] for word in line_words
        )

        reconstructed_lines.append({
            "text": line_text,
            "words": line_words,
            "block_num": key[0],
            "par_num": key[1],
            "line_num": key[2]
        })

    # Reconstruct paragraphs
    reconstructed_paragraphs = []

    for key, paragraph_words in paragraphs.items():

        paragraph_lines = {}

        for word in paragraph_words:

            line_key = word["line_num"]

            if line_key not in paragraph_lines:
                paragraph_lines[line_key] = []

            paragraph_lines[line_key].append(word["text"])

        paragraph_text = "\n".join(
            " ".join(line_words)
            for line_words in paragraph_lines.values()
        )

        reconstructed_paragraphs.append({
            "text": paragraph_text,
            "block_num": key[0],
            "par_num": key[1]
        })

    # Reconstruct complete text
    full_text = "\n\n".join(
        paragraph["text"]
        for paragraph in reconstructed_paragraphs
    )

    return {
        "text": full_text,
        "words": words,
        "lines": reconstructed_lines,
        "paragraphs": reconstructed_paragraphs
    }
