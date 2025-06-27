import gradio as gr
from PIL import Image, ImageDraw
import os
import uuid
import logging
import joblib

# Config
OUTPUT_DIR = "outputs"
MODEL_PATH = "model_assets/model.pkl"
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_image_from_text(prompt, model=None):
    image = Image.new("RGB", (512, 512), color="black")
    draw = ImageDraw.Draw(image)
    draw.text((10, 250), prompt, fill="white")
    return image

def load_model():
    try:
        return joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
    except Exception as e:
        logger.error(f"Model load error: {e}")
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
        logger.error(f"Error in prediction: {e}")
        return None, None

# Neobrutalist dark CSS
neo_dark_css = """
.gradio-container {
    font-family: 'Courier New', monospace;
    background: #111;
    color: white;
    border: 2px solid white;
}
button, input, .gr-button {
    border: 2px solid white;
    background-color: black;
    color: white;
    font-weight: bold;
}
"""

with gr.Blocks(css=neo_dark_css) as demo:
    gr.Markdown("# 🧱 Brutalist Text-to-Image Generator (Dark)")
    prompt = gr.Textbox(label="Prompt", placeholder="e.g. A spaceship built from coral")
    generate = gr.Button("MAKE IMAGE")
    image_out = gr.Image()
    download = gr.File(label="Save Image")

    generate.click(fn=predict, inputs=prompt, outputs=[image_out, download])

if __name__ == "__main__":
    demo.launch()
