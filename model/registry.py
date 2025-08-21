# model/registry.py
"""
Model registry for all supported tasks and providers.

- Register every available model (HF/local/API) as a ModelSpec.
- Select a default per task (TASK_DEFAULTS).
- Export MODEL_CONFIG for loader.py consumption.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional
import os
import logging

try:
    # Optional: your logger utility if present
    from utils.logger import setup_logger
    logger = setup_logger("model-registry")
except Exception:
    logger = logging.getLogger("model-registry")
    logging.basicConfig(level=logging.INFO)


# ──────────────────────────────────────────────────────────────
# Data structures
# ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ModelSpec:
    """Declarative description of a model."""
    name: str                 # Human-friendly name / key
    task: str                 # e.g. "text_to_text", "text_to_image", "text_to_video"
    source: str               # "huggingface" | "api" | "local"
    pipeline: str             # HF pipeline task or symbolic tag (e.g. "text-generation", "text-to-image", "custom")
    # One of the following should be provided depending on source:
    hf_id: Optional[str] = None     # huggingface repo id
    path: Optional[str] = None      # local path for "local"
    endpoint: Optional[str] = None  # API base/endpoint for "api"
    auth_env: Optional[str] = None  # env var that stores API key/token
    enabled: bool = True
    tags: Optional[List[str]] = None

    def to_loader_config(self) -> Dict:
        """
        Transform to the dict shape expected by loader.py
        """
        return {
            "source": self.source,
            "pipeline": self.pipeline,
            "name": self.hf_id or self.name,
            "path": self.path,
            "endpoint": self.endpoint,
            "auth_env": self.auth_env,
            "enabled": self.enabled,
            "task": self.task,
            "tags": self.tags or [],
        }


# ──────────────────────────────────────────────────────────────
# Registry (populate with safe defaults; extend as needed)
# ──────────────────────────────────────────────────────────────

MODEL_REGISTRY: Dict[str, ModelSpec] = {}

def register_model(spec: ModelSpec) -> None:
    if spec.name in MODEL_REGISTRY:
        logger.warning(f"Overriding existing model spec: {spec.name}")
    MODEL_REGISTRY[spec.name] = spec


# Default models (MVP focus: text_to_text, text_to_image, text_to_video)
# NOTE: API endpoints pulled from env so this file stays secret-free.
# You can later surface these via config UI.

# Text → Text (Hugging Face)
register_model(ModelSpec(
    name="mistral-7b-instruct",
    task="text_to_text",
    source="huggingface",
    pipeline="text-generation",
    hf_id="mistralai/Mistral-7B-Instruct-v0.2",
    tags=["llm", "instruct"]
))

register_model(ModelSpec(
    name="llama3-8b-instruct",
    task="text_to_text",
    source="huggingface",
    pipeline="text-generation",
    hf_id="meta-llama/Meta-Llama-3-8B-Instruct",
    tags=["llm", "instruct"]
))

# Text → Image (API placeholder; wire to your preferred provider)
register_model(ModelSpec(
    name="stability-sd-api",
    task="text_to_image",
    source="api",
    pipeline="text-to-image",
    endpoint=os.getenv("STABILITY_API_URL", "https://api.stability.ai/v2/generate"),
    auth_env="STABILITY_API_KEY",
    tags=["sd", "image-gen", "api"]
))

# (Optional) Text → Image via HF Diffusers backend name placeholder (requires diffusers-based loader)
register_model(ModelSpec(
    name="sdxl-hf",
    task="text_to_image",
    source="huggingface",
    pipeline="text-to-image",  # your loader should branch to diffusers for this
    hf_id="stabilityai/stable-diffusion-xl-base-1.0",
    tags=["sdxl", "diffusers"]
))

# Text → Video (API placeholder)
register_model(ModelSpec(
    name="runway-gen3-api",
    task="text_to_video",
    source="api",
    pipeline="text-to-video",
    endpoint=os.getenv("RUNWAY_API_URL", "https://api.runwayml.com/v1/generate"),
    auth_env="RUNWAY_API_KEY",
    tags=["video-gen", "api"]
))

# Alternative T2V API (example)
register_model(ModelSpec(
    name="pika-api",
    task="text_to_video",
    source="api",
    pipeline="text-to-video",
    endpoint=os.getenv("PIKA_API_URL", "https://api.pika.art/v1/generate"),
    auth_env="PIKA_API_KEY",
    tags=["video-gen", "api"]
))

# Local example (if you have a local fine-tuned model)
LOCAL_MODELS_DIR = Path(__file__).resolve().parent.parent / "model_assets"
if LOCAL_MODELS_DIR.exists():
    # Example: a local LLM folder
    local_llm_dir = LOCAL_MODELS_DIR / "local-llm"
    if local_llm_dir.exists():
        register_model(ModelSpec(
            name="local-llm",
            task="text_to_text",
            source="local",
            pipeline="text-generation",
            path=str(local_llm_dir),
            tags=["local"]
        ))


# ──────────────────────────────────────────────────────────────
# Defaults per task (can be overridden via env)
# ──────────────────────────────────────────────────────────────

TASK_DEFAULTS: Dict[str, str] = {
    "text_to_text": os.getenv("DEFAULT_T2T_MODEL", "mistral-7b-instruct"),
    "text_to_image": os.getenv("DEFAULT_T2I_MODEL", "stability-sd-api"),
    "text_to_video": os.getenv("DEFAULT_T2V_MODEL", "runway-gen3-api"),
    # Add other tasks here as you enable them
}


# ──────────────────────────────────────────────────────────────
# Public helpers
# ──────────────────────────────────────────────────────────────

def list_models(task: Optional[str] = None, source: Optional[str] = None, enabled: Optional[bool] = True) -> List[ModelSpec]:
    specs = list(MODEL_REGISTRY.values())
    if task:
        specs = [s for s in specs if s.task == task]
    if source:
        specs = [s for s in specs if s.source == source]
    if enabled is not None:
        specs = [s for s in specs if s.enabled == enabled]
    return specs

def get_model_spec(name: str) -> Optional[ModelSpec]:
    return MODEL_REGISTRY.get(name)

def get_default_spec(task: str) -> Optional[ModelSpec]:
    name = TASK_DEFAULTS.get(task)
    spec = MODEL_REGISTRY.get(name)
    if not spec:
        # Fallback: first enabled model for the task
        candidates = list_models(task=task, enabled=True)
        return candidates[0] if candidates else None
    return spec

def set_default_model(task: str, name: str) -> None:
    if name not in MODEL_REGISTRY:
        raise ValueError(f"Model '{name}' not found in registry.")
    if MODEL_REGISTRY[name].task != task:
        raise ValueError(f"Model '{name}' is not for task '{task}'.")
    TASK_DEFAULTS[task] = name
    logger.info(f"Default model for task '{task}' set to '{name}'")

def build_model_config() -> Dict[str, Dict]:
    """
    Build the compact config dict consumed by loader.py:
      MODEL_CONFIG[task] -> { source, pipeline, name, path, endpoint, auth_env, ... }
    """
    config: Dict[str, Dict] = {}
    tasks = {spec.task for spec in MODEL_REGISTRY.values()}
    for task in tasks:
        spec = get_default_spec(task)
        if spec and spec.enabled:
            config[task] = spec.to_loader_config()
    return config


# ──────────────────────────────────────────────────────────────
# Export: MODEL_CONFIG for loader.py
# ──────────────────────────────────────────────────────────────

MODEL_CONFIG: Dict[str, Dict] = build_model_config()
logger.info(f"MODEL_CONFIG ready with tasks: {list(MODEL_CONFIG.keys())}")

