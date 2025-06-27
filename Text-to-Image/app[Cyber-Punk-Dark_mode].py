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

def generate_image_from_text(prompt, model=None):
    image = Image.new("RGB", (512, 512), color="black")
    draw = ImageDraw.Draw(image)
    draw.text((10, 250), prompt, fill="#39ff14")
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
        logger.error(f"Prediction error: {e}")
        return None, None

cyber_dark_css = """
.gradio-container {
    background-color: #0f0f0f;
    color: #39ff14;
    font-family: 'Orbitron', sans-serif;
}
button, input, .gr-button {
    background-color: #1a1a1a;
    color: #39ff14;
    border: 2px solid #39ff14;
    font-weight: bold;
    border-radius: 5px;
}
"""

with gr.Blocks(css=cyber_dark_css) as demo:
    gr.Markdown("## 🌌 Cyberpunk T2I Generator (Dark Mode)")
    prompt = gr.Textbox(label="Prompt: Describe a scene 👾")
    generate = gr.Button("🚀 Synthesize")
    output_img = gr.Image()
    download = gr.File(label="Save")

    generate.click(fn=predict, inputs=prompt, outputs=[output_img, download])

if __name__ == "__main__":
    demo.launch()
