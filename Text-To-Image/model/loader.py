import os
import logging
import joblib
from functools import lru_cache
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
    AutoModelForImageClassification,
    AutoModelForSeq2SeqLM,
)

from config.settings import MODEL_OPTIONS

logger = logging.getLogger("gradio-template")

# ───────────────────────────────────────────── #
# ✅ Utility Functions
# ───────────────────────────────────────────── #

def is_valid_model_name(model_name: str) -> bool:
    return model_name in MODEL_OPTIONS

def is_joblib_model(path: str) -> bool:
    return path.endswith(".pkl") and os.path.exists(path)

def is_huggingface_model(model_id: str) -> bool:
    return "/" in model_id

# ───────────────────────────────────────────── #
# 🔁 Traditional ML Models (.pkl via Joblib)
# ───────────────────────────────────────────── #

@lru_cache(maxsize=8)
def load_joblib_model(model_name: str):
    """
    Loads a traditional ML model using joblib.
    """
    try:
        if not is_valid_model_name(model_name):
            raise ValueError(f"❌ Invalid model name: {model_name}")

        model_path = MODEL_OPTIONS[model_name]
        if not is_joblib_model(model_path):
            raise ValueError(f"❌ Not a valid .pkl file: {model_path}")

        model = joblib.load(model_path)
        logger.info(f"[✓] Loaded joblib model: {model_name}")
        return model

    except Exception as e:
        logger.error(f"[x] Failed to load joblib model '{model_name}': {e}")
        return None

# ───────────────────────────────────────────── #
# 🔁 Hugging Face Transformers (LLMs, Vision)
# ───────────────────────────────────────────── #

@lru_cache(maxsize=4)
def load_huggingface_model(model_id: str, task: str = "text-generation"):
    """
    Loads a Hugging Face model pipeline.
    Supports `text-generation`, `text2text-generation`, `image-classification`.
    """
    try:
        logger.info(f"🔁 Loading HF model [{task}]: {model_id}")

        tokenizer = AutoTokenizer.from_pretrained(model_id)

        if task == "text-generation":
            model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto")
        elif task == "text2text-generation":
            model = AutoModelForSeq2SeqLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto")
        elif task == "image-classification":
            model = AutoModelForImageClassification.from_pretrained(model_id)
        else:
            raise ValueError(f"Unsupported Hugging Face task: {task}")

        pipe = pipeline(task, model=model, tokenizer=tokenizer)
        logger.info(f"[✓] Hugging Face model ready: {model_id}")
        return pipe

    except Exception as e:
        logger.error(f"[x] Failed to load HF model '{model_id}': {e}")
        return None

# ───────────────────────────────────────────── #
# 📦 Entry Point Loader (Auto)
# ───────────────────────────────────────────── #

def load_model(model_name: str):
    """
    Auto-loads model from MODEL_OPTIONS config.
    Detects and routes to correct loader.
    """
    try:
        if not is_valid_model_name(model_name):
            raise ValueError(f"Model '{model_name}' not found.")

        model_path = MODEL_OPTIONS[model_name]

        if is_joblib_model(model_path):
            return load_joblib_model(model_name)

        elif is_huggingface_model(model_path):
            return load_huggingface_model(model_path)

        else:
            raise ValueError("Unsupported model format or path.")

    except Exception as e:
        logger.error(f"❌ Failed to auto-load model '{model_name}': {e}")
        return None

# ───────────────────────────────────────────── #
# 📋 Helper: List Available Models
# ───────────────────────────────────────────── #

def list_available_models():
    """Returns available model names for UI dropdowns."""
    return list(MODEL_OPTIONS.keys())
