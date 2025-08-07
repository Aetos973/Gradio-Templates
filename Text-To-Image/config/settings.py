import os
from pathlib import Path

# ───── Base Directories ───── #
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "template"
MODELS_DIR = BASE_DIR / "model_assets"

# ───── Theme Config (Dynamic) ───── #
THEMES = {
    os.path.splitext(f)[0].replace("_", " ").title(): TEMPLATES_DIR / f
    for f in os.listdir(TEMPLATES_DIR)
    if f.endswith(".css")
}
DEFAULT_THEME = "Classic Dark"

# ───── Model Config (Dynamic) ───── #
MODEL_OPTIONS = {
    os.path.splitext(f)[0]: MODELS_DIR / f
    for f in os.listdir(MODELS_DIR)
    if f.endswith(".pkl")
}
DEFAULT_MODEL = list(MODEL_OPTIONS.keys())[0] if MODEL_OPTIONS else None

# ───── Security ───── #
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# ───── General Settings ───── #
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SHOW_PROGRESS_BAR = True  # optional toggle for UI feedback
