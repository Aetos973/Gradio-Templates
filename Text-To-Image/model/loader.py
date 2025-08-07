import joblib
import logging
from config.settings import MODEL_OPTIONS

logger = logging.getLogger("gradio-template")

def load_model(model_name: str):
    """Loads model by name from config"""
    try:
        if model_name not in MODEL_OPTIONS:
            logger.warning(f"Model '{model_name}' not found. Using fallback.")
            return None

        model_path = MODEL_OPTIONS[model_name]
        model = joblib.load(model_path)
        logger.info(f"Loaded model: {model_name}")
        return model
    except Exception as e:
        logger.error(f"Error loading model '{model_name}': {e}")
        return None
