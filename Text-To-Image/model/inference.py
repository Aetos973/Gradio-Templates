from PIL import Image, ImageDraw
import uuid
import os
import logging

logger = logging.getLogger("gradio-template")
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_image_from_text(prompt, model=None):
    """Placeholder image generation."""
    logger.info("Generating image...")
    image = Image.new("RGB", (512, 512), color="black")
    draw = ImageDraw.Draw(image)
    draw.text((10, 250), prompt, fill="white")
    return image

def predict(prompt, model):
    try:
        image = generate_image_from_text(prompt, model)
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image output")

        file_id = str(uuid.uuid4())
        path = os.path.join(OUTPUT_DIR, f"{file_id}.png")
        image.save(path)
        logger.info(f"Saved: {path}")
        return image, path
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return None, None
