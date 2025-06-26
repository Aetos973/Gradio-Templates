import gradio as gr
from PIL import Image
import random
import logging
import os
import joblib

# === Setup Logging ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("text_to_image.log"),
        logging.StreamHandler()
    ]
)

# === Load Model ===
def load_model(model_path="model.pkl"):
    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at: {model_path}")
        model = joblib.load(model_path)
        logging.info("✅ Model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"❌ Failed to load model: {e}")
        return None

# Dummy placeholder function (replace with actual inference)
def dummy_text_to_image(prompt):
    logging.info(f"🔍 Received prompt: {prompt}")
    img = Image.new("RGB", (256, 256), (
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    )
    logging.info("🖼️ Returning dummy image.")
    return img

model = load_model()

# === Gradio Interface ===
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🖼️ Text to Image Generator - Minimal (Light Mode)")
    prompt = gr.Textbox(placeholder="Enter your prompt here", label="Prompt")
    output = gr.Image(label="Generated Image", type="pil")
    generate = gr.Button("Generate")

    generate.click(fn=dummy_text_to_image, inputs=prompt, outputs=output)

demo.launch()
