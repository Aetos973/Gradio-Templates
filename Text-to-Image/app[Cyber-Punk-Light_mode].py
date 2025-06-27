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

# ───── Dummy Generator ───── #
def generate_image_from_text(prompt, model=None):
    image = Image.new("RGB", (512, 512), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 250), prompt, fill="#ff00cc")
    return image

# ───── Load Model ───── #
def load_model():
    try:
        return joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
    except Exception as e:
        logger.error(f"Model load error: {e}")
        return None

model = load_model()

# ───── Prediction Logic ───── #
def predict(prompt):
    try:
        image = generate_image_from_text(prompt, model)
        image_id = str(uuid.uuid4())
        output_path = os.path.join(OUTPUT_DIR, f"{image_id}.png")
        image.save(output_path)
        return image, output_path
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return None, None

# ───── CSS ───── #
cyber_light_css = """
.gradio-container {
    background: linear-gradient(135deg, #f0f0f0, #fafafa);
    color: #ff00cc;
    font-family: 'Orbitron', sans-serif;
}
button, input, .gr-button {
    background-color: #ffffff;
    color: #ff00cc;
    border: 2px solid #ff00cc;
    font-weight: bold;
    border-radius: 5px;
}
"""

# ───── UI ───── #
with gr.Blocks(css=cyber_light_css) as demo:
    gr.Markdown("## 🌐 Cyberpunk T2I Generator (Light Mode)")
    prompt = gr.Textbox(label="Describe your neon dream 💭")
    generate = gr.Button("⚡ Generate")
    output_img = gr.Image()
    download = gr.File(label="Download")

    generate.click(fn=predict, inputs=prompt, outputs=[output_img, download])

if __name__ == "__main__":
    demo.launch()
