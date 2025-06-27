import gradio as gr
from PIL import Image, ImageDraw
import os
import uuid
import logging
import joblib

# ───── Configuration ───── #
OUTPUT_DIR = "outputs"
MODEL_PATH = "model_assets/model.pkl"

# ───── Setup ───── #
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ───── Dummy Placeholder Model ───── #
def generate_image_from_text(prompt, model=None):
    logger.info("Running placeholder image generator...")
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
            logger.warning(f"Model not found at {MODEL_PATH}. Using default placeholder.")
            model = None
        return model
    except Exception as e:
        logger.error(f"Model loading failed: {e}")
        return None

model = load_model()

# ───── Prediction Logic ───── #
def predict(prompt):
    try:
        logger.info(f"Prompt received: {prompt}")
        image = generate_image_from_text(prompt, model=model)

        if not isinstance(image, Image.Image):
            raise ValueError("Output is not a valid image.")

        image_id = str(uuid.uuid4())
        path = os.path.join(OUTPUT_DIR, f"{image_id}.png")
        image.save(path)
        logger.info(f"Image saved at: {path}")

        return image, path

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return None, None

# ───── Gradio UI ───── #
with gr.Blocks(theme=gr.themes.Base(), css=".gradio-container { background-color: #1c1c1c; color: white; }") as demo:
    gr.Markdown("## 🌌 Text-to-Image Generator (Modern Dark Theme)")
    with gr.Row():
        prompt_input = gr.Textbox(label="Enter a prompt", placeholder="e.g. A nebula shaped like a lion")
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
