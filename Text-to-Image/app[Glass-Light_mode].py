import gradio as gr
from PIL import Image, ImageDraw
import os
import uuid
import logging
import joblib

# ───── Configuration ───── #
OUTPUT_DIR = "outputs"
MODEL_PATH = "model_assets/model.pkl"
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ───── Dummy Image Generator ───── #
def generate_image_from_text(prompt, model=None):
    logger.info("Generating placeholder image...")
    image = Image.new("RGB", (512, 512), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 250), prompt, fill="black")
    return image

# ───── Model Loader ───── #
def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            logger.info("Model loaded.")
        else:
            logger.warning("Model not found. Using None.")
            model = None
        return model
    except Exception as e:
        logger.error(f"Model load error: {e}")
        return None

model = load_model()

# ───── Prediction ───── #
def predict(prompt):
    try:
        image = generate_image_from_text(prompt, model)
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image.")

        image_id = str(uuid.uuid4())
        path = os.path.join(OUTPUT_DIR, f"{image_id}.png")
        image.save(path)
        return image, path
    except Exception as e:
        logger.error(f"Inference error: {e}")
        return None, None

# ───── Gradio UI ───── #
glass_css = """
.gradio-container {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(12px);
    border-radius: 12px;
    padding: 20px;
    font-family: 'Segoe UI', sans-serif;
    color: #222;
}
"""

with gr.Blocks(css=glass_css) as demo:
    gr.Markdown("### 🧊 Text-to-Image Generator (Glassmorphic Light UI)")
    with gr.Row():
        prompt_input = gr.Textbox(label="Prompt", placeholder="e.g. A sunset over crystal mountains")
    with gr.Row():
        generate_button = gr.Button("Generate")
    with gr.Row():
        image_output = gr.Image(label="Generated Image")
        download_button = gr.File(label="Download Image")

    generate_button.click(fn=predict, inputs=prompt_input, outputs=[image_output, download_button])

if __name__ == "__main__":
    demo.launch()
