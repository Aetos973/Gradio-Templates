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

# ───── Dummy Model ───── #
def generate_image_from_text(prompt, model=None):
    logger.info("Generating placeholder image...")
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
            logger.warning("Model not found, using placeholder.")
            model = None
        return model
    except Exception as e:
        logger.error(f"Model loading error: {e}")
        return None

model = load_model()

def predict(prompt):
    try:
        logger.info(f"Prompt: {prompt}")
        image = generate_image_from_text(prompt, model)
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image output.")

        image_id = str(uuid.uuid4())
        path = os.path.join(OUTPUT_DIR, f"{image_id}.png")
        image.save(path)
        logger.info(f"Saved to {path}")
        return image, path
    except Exception as e:
        logger.error(f"Inference error: {e}")
        return None, None

# ───── Gradio UI ───── #
with gr.Blocks(theme=gr.themes.Default(), css=".gradio-container { background-color: #111; color: white; }") as demo:
    gr.Markdown("## 🌑 Classic Text-to-Image Generator (Dark Mode)")
    with gr.Row():
        with gr.Column(scale=1):
            prompt_input = gr.Textbox(label="Text Prompt", placeholder="e.g. A castle in the clouds")
            generate_btn = gr.Button("Generate")
            clear_btn = gr.Button("Clear")
        with gr.Column(scale=2):
            output_image = gr.Image(label="Image")
            download_button = gr.File(label="Download")

    def run(prompt): return predict(prompt)
    def clear(): return "", None, None

    generate_btn.click(run, inputs=prompt_input, outputs=[output_image, download_button])
    clear_btn.click(clear, outputs=[prompt_input, output_image, download_button])

if __name__ == "__main__":
    demo.launch()
