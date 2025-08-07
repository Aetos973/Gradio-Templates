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

# ───── Hugging Face Mistral Client ───── #
@lru_cache(maxsize=1)
def get_mistral_client(model_id="mistralai/Mistral-7B-Instruct-v0.2"):
    """
    Load a Hugging Face transformer-based model.
    Caches the pipeline for performance.
    """
    try:
        logger.info(f"🔁 Loading Hugging Face model: {model_id}")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id, device_map="auto", torch_dtype="auto"
        )
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
        logger.info("✅ Mistral client initialized.")
        return pipe

    except Exception as e:
        logger.error(f"🚨 Failed to load Hugging Face model '{model_id}': {e}")
        return None

# ───── Prompt Formatter Using Mistral ───── #
def transform_prompt(raw_prompt: str, metadata: dict):
    """
    Use Mistral to transform a user's natural prompt into a system-optimized one.
    `metadata` includes: mood, type, art_style, image_type, frame, temperature, etc.
    """
    try:
        pipe = get_mistral_client()
        if not pipe:
            raise RuntimeError("Hugging Face model not available")

        instruction = (
            f"Transform the following prompt for a generative image model.\n"
            f"Ensure it's concise, highly descriptive, and tailored to this context:\n"
            f"- Mood: {metadata.get('mood')}\n"
            f"- Type: {metadata.get('type')}\n"
            f"- Art Style: {metadata.get('art_style')}\n"
            f"- Image Type: {metadata.get('image_type')}\n"
            f"- Frame: {metadata.get('frame')}\n\n"
            f"User Prompt: {raw_prompt}\n\n"
            f"Optimized Prompt:"
        )

        result = pipe(instruction, max_new_tokens=150, do_sample=True, temperature=metadata.get("temperature", 0.7))
        optimized = result[0]["generated_text"].split("Optimized Prompt:")[-1].strip()
        logger.info("✨ Prompt transformed successfully.")
        return optimized

    except Exception as e:
        logger.error(f"[x] Prompt transformation failed: {e}")
        return raw_prompt  # Fallback to original prompt

# ───── Model Names for UI / CLI ───── #
def list_available_models():
    """Returns available model names from local directory."""
    return list(MODEL_OPTIONS.keys())
