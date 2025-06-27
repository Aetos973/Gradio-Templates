import gradio as gr
from PIL import Image, ImageDraw
import os
import uuid
import logging
import joblib

# Setup
OUTPUT_DIR = "outputs"
MODEL_PATH = "model_assets/model.pkl"
os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dummy model
def generate_image_from_text(prompt, model=None):
    image = Image.new("RGB", (512, 512), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 250), prompt, fill="black")
    return image

# Model loader
def load_model():
    try:
        if os.path.exists(MODEL_PATH):
            return joblib.load(MODEL_PATH)
        logger.warning("No model found. Using default.")
        return None
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None

model = load_model()

# Prediction logic
def predict(prompt):
    try:
        image = generate_image_from_text(prompt, model)
        image_id = str(uuid.uuid4())
        path = os.path.join(OUTPUT_DIR, f"{image_id}.png")
        image.save(path)
        return image, path
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return None, None

# Brutalist light CSS
neo_light_css = """
.gradio-container {
    font-family: 'Courier New', monospace;
    background: #fdfdfd;
    color: #111;
    border: 2px solid #111;
}
button, input, .gr-button {
    border: 2px solid black;
    background-color: white;
    color: black;
    font-weight: bold;
}
"""

# Gradio UI
with gr.Blocks(css=neo_light_css) as demo:
    gr.Markdown("# 🧱 Brutalist Text-to-Image Generator (Light)")
    prompt = gr.Textbox(label="Prompt", placeholder="Type your idea...")
    generate = gr.Button("GENERATE")
    image_out = gr.Image()
    download = gr.File(label="Download Result")

    generate.click(fn=predict, inputs=prompt, outputs=[image_out, download])

if __name__ == "__main__":
    demo.launch()
