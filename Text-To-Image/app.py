import gradio as gr
import logging
from model.loader import get_mistral_client
from model.inference import build_prompt_instruction
from config.ui_config import UI_CONFIG
from config.settings import MODEL_OPTIONS

logger = logging.getLogger("gradio-template")

# ───── Function: Process Prompt and Generate ───── #
def generate_image(user_prompt, mood, prompt_type, art_style, image_type, frame, model_choice):
    # Step 1: Create metadata
    metadata = {
        "mood": mood,
        "type": prompt_type,
        "art_style": art_style,
        "image_type": image_type,
        "frame": frame
    }

    # Step 2: Build instruction prompt
    instruction = build_prompt_instruction(user_prompt, metadata)

    # Step 3: Get Mistral client and generate optimized prompt
    mistral = get_mistral_client()
    if mistral is None:
        return "Error loading Mistral."

    try:
        result = mistral(instruction, max_new_tokens=150, do_sample=True, temperature=0.7)
        optimized_prompt = result[0]['generated_text'].split("Optimized Prompt:")[-1].strip()
    except Exception as e:
        logger.error(f"Prompt transformation failed: {e}")
        optimized_prompt = user_prompt  # fallback

    # TODO: Use optimized_prompt with selected image model (not implemented yet)
    return f"🔁 Optimized Prompt:\n{optimized_prompt}"


# ───── Gradio UI Elements ───── #
with gr.Blocks(title="Gradio Image Prompt Optimizer") as demo:
    gr.Markdown("## 🧠 AI-Powered Prompt Enhancer")

    with gr.Row():
        user_prompt = gr.Textbox(label="Describe Your Image", placeholder="e.g. A dragon flying over a neon city at night")

    with gr.Row():
        mood = gr.Dropdown(choices=UI_CONFIG["mood"], label="Mood", value=UI_CONFIG["mood"][0])
        prompt_type = gr.Dropdown(choices=UI_CONFIG["type"], label="Prompt Type", value=UI_CONFIG["type"][0])
        art_style = gr.Dropdown(choices=UI_CONFIG["art_style"], label="Art Style", value=UI_CONFIG["art_style"][0])
    
    with gr.Row():
        image_type = gr.Dropdown(choices=UI_CONFIG["image_type"], label="Image Type", value=UI_CONFIG["image_type"][0])
        frame = gr.Dropdown(choices=UI_CONFIG["frame"], label="Frame", value=UI_CONFIG["frame"][0])
        model_choice = gr.Dropdown(choices=list(MODEL_OPTIONS.keys()), label="Model", value=list(MODEL_OPTIONS.keys())[0])

    generate_btn = gr.Button("⚡ Generate Optimized Prompt")

    output_text = gr.Textbox(label="Optimized Prompt", lines=6)

    generate_btn.click(
        fn=generate_image,
        inputs=[user_prompt, mood, prompt_type, art_style, image_type, frame, model_choice],
        outputs=[output_text]
    )

# ───── Launch App ───── #
if __name__ == "__main__":
    demo.launch()
