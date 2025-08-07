import os
import logging
import joblib
from functools import lru_cache
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config.settings import MODEL_OPTIONS

logger = logging.getLogger("gradio-template")

# ───── Load Traditional Joblib Model ───── #
def load_model_by_name(model_name: str):
    """
    Load a model from MODEL_OPTIONS dict.
    Supports traditional ML (.pkl) models.
    """
    try:
        if model_name not in MODEL_OPTIONS:
            raise ValueError(f"Model '{model_name}' not found in settings.")

        model_path = MODEL_OPTIONS[model_name]
        if not model_path.endswith(".pkl"):
            raise ValueError("Invalid model type. Only .pkl supported here.")

        model = joblib.load(model_path)
        logger.info(f"[✓] Loaded joblib model: {model_name}")
        return model

    except Exception as e:
        logger.error(f"[x] Failed to load model '{model_name}': {e}")
        return None

# ───── Mistral or Hugging Face Client ───── #
@lru_cache(maxsize=1)
def get_mistral_client(model_id="mistralai/Mistral-7B-Instruct-v0.2"):
    """
    Load a Hugging Face transformer-based model.
    Caches the pipeline for performance.
    """
    try:
        logger.info(f"🔁 Loading Hugging Face model: {model_id}")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto")
        
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
        logger.info("✅ Mistral client initialized.")
        return pipe

    except Exception as e:
        logger.error(f"🚨 Failed to load Hugging Face model '{model_id}': {e}")
        return None

# ───── Available Models Summary ───── #
def list_available_models():
    """Returns the available model names for dropdowns or CLI."""
    return list(MODEL_OPTIONS.keys())
