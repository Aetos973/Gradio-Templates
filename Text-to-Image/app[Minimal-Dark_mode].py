import gradio as gr
from PIL import Image, ImageDraw
import os
import uuid
import logging
import joblib

# ───── Configuration ───── #
OUTPUT_DIR = "outputs"
MODEL_PATH = "model_assets/model.pkl"  # Placeholder path

# ───── Setup ───── #
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ───── Dummy Placeholder Model ───── #
def generate_image_from_text(prompt, model=None):
    logger.info("Running placeholder image generator...")

    # Create a simple black background image with white text
    image = Image.new("RGB", (512, 512), color="black")
    draw = ImageDraw.Draw(image)
    draw.text((10, 250), prompt, fill="white")
    return image

# ───── Load Model ───── #
def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            logger.info("Model loaded successfully.")
        else:
            logger.warning(f"Model file not found at: {MODEL_PATH}. Using None.")
            model = None
        return model
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return None

model = load_model()

# ───── Prediction Logic ───── #
def predict(prompt):
    try:
        logger.info(f"Received prompt: {prompt}")
        image = generate_image_from_text(prompt, model=model)

        if not isinstance(image, Image.Image):
            raise ValueError("Generated output is not a valid image.")

        image_id = str(uuid.uuid4())
        output_path = os.path.join(OUTPUT_DIR, f"{image_id}.png")
        image.save(output_path)
        logger.info(f"Image saved to: {output_path}")

        return image, output_path

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return None, None

# ───── Gradio UI ───── #
with gr.Blocks(theme=gr.themes.Base(), css=".gradio-container { background-color: #1c1c1c; color: white; }") as demo:
    gr.Markdown("## 🌌 Text-to-Image Generator (Minimal, Dark Mode)")
    with gr.Row():
        prompt_input = gr.Textbox(label="Enter a text prompt", placeholder="e.g. A neon dragon flying through space")
    with gr.Row():
        generate_btn = gr.Button("Generate Image")
    with gr.Row():
        output_image = gr.Image(label="Generated Image")
        download_button = gr.File(label="Download Image")

    def run(prompt):
        return predict(prompt)

    generate_btn.click(fn=run, inputs=prompt_input, outputs=[output_image, download_button])

if __name__ == "__main__":
    demo.launch()
