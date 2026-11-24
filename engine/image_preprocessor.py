from pathlib import Path
from PIL import Image, ImageOps

MAX_IMAGE_PIXELS = 30000000

def preprocess_image(image_path):

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError("Image does not exist")

    with Image.open(image_path) as image:

        width, height = image.size

        if width * height > MAX_IMAGE_PIXELS:
            raise ValueError("Image resolution is too large")

        image = ImageOps.exif_transpose(image)

        if image.mode in ("RGBA", "LA") or "transparency" in image.info:

            image = image.convert("RGBA")

            background = Image.new("RGB", image.size, "white")

            background.paste(image, mask=image.getchannel("A"))

            image = background

        else:

            image = image.convert("RGB")

        output_dir = Path("outputs/processed")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{image_path.stem}_processed.png"

        image.save(output_path, format="PNG")

    return output_path