import gradio as gr
from PIL import Image, ImageDraw
import os
import uuid
import logging
import joblib

OUTPUT_DIR = "outputs"
MODEL_PATH = "model_assets/model.pkl"
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_image_from_text(prompt, model=None):
    logger.info("Generating image...")
    image = Image.new("RGB", (512, 512), color="black")
    draw = ImageDraw.Draw(image)
    draw.text((10, 250), prompt, fill="white")
    return image

def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            logger.info("Model loaded.")
        else:
            model = None
            logger.warning("Model not found.")
        return model
    except Exception as e:
        logger.error(f"Model error: {e}")
        return None

model = load_model()

def predict(prompt):
    try:
        image = generate_image_from_text(prompt, model)
        image_id = str(uuid.uuid4())
        path = os.path.join(OUTPUT_DIR, f"{image_id}.png")
        image.save(path)
        return image, path
    except Exception as e:
        logger.error(f"Inference issue: {e}")
        return None, None

glass_dark_css = """
.gradio-container {
    background: rgba(30, 30, 30, 0.75);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    color: #eee;
    font-family: 'Fira Code', monospace;
}
"""

with gr.Blocks(css=glass_dark_css) as demo:
    gr.Markdown("### 🧊 Text-to-Image Generator (Glassmorphic Dark UI)")
    with gr.Row():
        prompt_input = gr.Textbox(label="Prompt", placeholder="e.g. A futuristic city under moonlight")
    with gr.Row():
        generate_button = gr.Button("Generate Image")
    with gr.Row():
        image_output = gr.Image(label="Result")
        download_button = gr.File(label="Download")

    generate_button.click(fn=predict, inputs=prompt_input, outputs=[image_output, download_button])

if __name__ == "__main__":
    demo.launch()
