def get_status_message(prompt, model_name):
    if not prompt:
        return "⛔ Please enter a text prompt."
    return f"⏳ Generating image using **{model_name}**..."
