import gradio as gr
from config.settings import THEMES, MODEL_OPTIONS, DEFAULT_THEME, DEFAULT_MODEL
from model.loader import load_model
from model.inference import predict
from utils.logger import setup_logger
from utils.tracker import get_status_message

logger = setup_logger()

# ───── Load default model ───── #
active_model = load_model(DEFAULT_MODEL)

# ───── Load selected CSS ───── #
def load_css(theme_name):
    with open(THEMES[theme_name], "r") as f:
        return f.read()

# ───── Gradio App ───── #
with gr.Blocks(css=load_css(DEFAULT_THEME)) as demo:
    gr.Markdown("## 🖼️ Text-to-Image Generator")

    with gr.Row():
        theme_dropdown = gr.Dropdown(label="Choose Theme", choices=list(THEMES.keys()), value=DEFAULT_THEME)
        model_dropdown = gr.Dropdown(label="Choose Model", choices=list(MODEL_OPTIONS.keys()), value=DEFAULT_MODEL)

    prompt_input = gr.Textbox(label="Prompt", placeholder="e.g. A neon samurai in the rain")
    generate_btn = gr.Button("Generate")
    clear_btn = gr.Button("Clear")

    with gr.Row():
        output_image = gr.Image(label="Generated Image")
        download_file = gr.File(label="Download")
    
    status_tracker = gr.Markdown("")  # UX status updates

    # ───── Function Hooks ───── #
    def run(prompt, model_name):
        global active_model
        status = get_status_message(prompt, model_name)
        active_model = load_model(model_name)
        image, path = predict(prompt, active_model)
        return image, path, status

    def clear():
        return "", None, None, ""

    def switch_theme(theme_name):
        return gr.update(css=load_css(theme_name))

    # ───── Bind Events ───── #
    generate_btn.click(run, inputs=[prompt_input, model_dropdown], outputs=[output_image, download_file, status_tracker])
    clear_btn.click(clear, outputs=[prompt_input, output_image, download_file, status_tracker])
    theme_dropdown.change(fn=switch_theme, inputs=theme_dropdown, outputs=[])

if __name__ == "__main__":
    demo.launch()
