import uuid
import os
import logging
from PIL import Image, ImageDraw
from config.settings import DEFAULT_MODEL
from model.loader import load_model_by_name, get_mistral_client

# ───── Config ───── #
logger = logging.getLogger("gradio-template")
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ───── Prompt Transformation ───── #
def transform_prompt_with_mistral(prompt: str, category: str = "wallpaper", mood: str = "aesthetic") -> str:
    """
    Transforms the user's raw prompt using the Mistral prompt transformer model.
    Returns a refined prompt suitable for image generation.
    """
    client = get_mistral_client()
    if client is None:
        logger.warning("Mistral client unavailable. Using raw prompt.")
        return prompt

    try:
        system_prompt = f"You are a prompt engineer. Convert the user's input into a highly descriptive and creative prompt for generating a {category} with a {mood} tone."
        response = client.text_generation(
            prompt=f"<s>[INST] {system_prompt} User: {prompt} [/INST]",
            max_new_tokens=150,
            temperature=0.7,
            top_p=0.9
        )
        return response.strip()
    except Exception as e:
        logger.error(f"Mistral prompt transformation failed: {e}")
        return prompt

# ───── Image Generation ───── #
def generate_image_from_text(prompt: str, model):
    """
    Generate image using the provided model.
    Replace this stub with actual model inference logic (e.g., StableDiffusion).
    """
    try:
        logger.info("Simulating image generation...")
        image = Image.new("RGB", (512, 512), color="black")
        draw = ImageDraw.Draw(image)
        draw.text((10, 250), prompt, fill="white")
        return image
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        return None

# ───── Main Prediction Logic ───── #
def predict(prompt: str, model_name: str = DEFAULT_MODEL, category="wallpaper", mood="aesthetic"):
    try:
        # Transform prompt first
        refined_prompt = transform_prompt_with_mistral(prompt, category, mood)
        logger.info(f"Transformed Prompt: {refined_prompt}")

        # Load selected generation model
        model = load_model_by_name(model_name)
        if model is None:
            raise RuntimeError(f"Failed to load model: {model_name}")

        # Generate image
        image = generate_image_from_text(refined_prompt, model)
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image output")

        # Save image
        file_id = str(uuid.uuid4())
        path = os.path.join(OUTPUT_DIR, f"{file_id}.png")
        image.save(path)
        logger.info(f"Image saved to: {path}")
        return image, path

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return None, None
