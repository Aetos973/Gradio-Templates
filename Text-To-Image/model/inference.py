import os
import logging
import joblib
from functools import lru_cache
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from config.settings import MODEL_OPTIONS
from config.ui_config import UI_CONFIG  # 🔥 NEW

logger = logging.getLogger("gradio-template")

# ───── Load Traditional Joblib Model ───── #
def load_model_by_name(model_name: str):
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

# ───── Hugging Face Transformer Loader ───── #
@lru_cache(maxsize=1)
def get_mistral_client(model_id="mistralai/Mistral-7B-Instruct-v0.2"):
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

# ───── Model Summary ───── #
def list_available_models():
    return list(MODEL_OPTIONS.keys())

# ───── Prompt Instruction Template ───── #
def build_prompt_instruction(raw_prompt: str, metadata: dict) -> str:
    """
    Build a structured prompt instruction using the enhanced metadata.
    """
    try:
        mood = metadata.get("mood", "Default")
        art_style = metadata.get("art_style", "Realism")
        image_type = metadata.get("image_type", "Icon")
        frame = metadata.get("frame", "Square")
        prompt_type = metadata.get("type", "General")

        instruction = (
            f"Transform the following prompt for a generative image model.\n"
            f"Ensure it's concise, highly descriptive, and tailored to this context:\n"
            f"- Mood: {mood}\n"
            f"- Type: {prompt_type}\n"
            f"- Art Style: {art_style}\n"
            f"- Image Type: {image_type}\n"
            f"- Frame: {frame}\n\n"
            f"User Prompt: {raw_prompt}\n\n"
            f"Optimized Prompt:"
        )
        return instruction

    except Exception as e:
        logger.error(f"[x] Failed to build instruction: {e}")
        return f"User Prompt: {raw_prompt}\nOptimized Prompt:"
