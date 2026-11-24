from pathlib import Path
import cariosvg

SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png", ".svg"]

def validate_image(image_path):
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image file '{image_path}' does not exist.")
    if not image_path.is_file():
        raise ValueError(f"'{image_path}' is not a valid file.")
    extension = image_path.suffix.lower()

    if extension not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported image format '{extension}'. Supported formats are: {', '.join(SUPPORTED_FORMATS)}.")

    return image_path



def convert_svg_to_png(svg_path, output_path):
    output_path = Path("output")/ f"{output_path.stem}.png"

    cariosvg.svg2png(
        url=str(svg_path), 
        write_to=str(output_path))
    return output_path

def process_image(image_path):

    image_path = validate_image(image_path)

    if image_path.suffix.lower() == ".svg":

        image_path = convert_svg_to_png(image_path)

    return image_path