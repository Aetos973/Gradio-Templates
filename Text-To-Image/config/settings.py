import os

# ───── Theme Config ───── #
TEMPLATES_DIR = "templates"
THEMES = {
    os.path.splitext(f)[0].replace("_", " ").title(): os.path.join(TEMPLATES_DIR, f)
    for f in os.listdir(TEMPLATES_DIR)
    if f.endswith(".css")
}

# ───── Model Config ───── #
MODELS_DIR = "model_assets"
MODEL_OPTIONS = {
    os.path.splitext(f)[0]: os.path.join(MODELS_DIR, f)
    for f in os.listdir(MODELS_DIR)
    if f.endswith(".pkl")
}

DEFAULT_THEME = "Classic Dark"
DEFAULT_MODEL = list(MODEL_OPTIONS.keys())[0] if MODEL_OPTIONS else None
