"""
loader.py
Responsible for loading AI models dynamically based on config/settings.py
Supports local models, Hugging Face, and API endpoints.
"""

import os
from config.settings import MODEL_CONFIG
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

class ModelLoader:
    def __init__(self):
        self.models = {}

    def load_model(self, task: str):
        """
        Loads a model for the given task if not already loaded.
        """
        if task in self.models:
            return self.models[task]

        if task not in MODEL_CONFIG:
            raise ValueError(f"No model configuration found for task: {task}")

        cfg = MODEL_CONFIG[task]

        if cfg["source"] == "huggingface":
            print(f"🔄 Loading HuggingFace model: {cfg['name']} for task {task}")
            model = pipeline(
                cfg["pipeline"],
                model=cfg["name"],
                device=0 if torch.cuda.is_available() else -1
            )
        elif cfg["source"] == "local":
            print(f"📂 Loading local model from {cfg['path']}")
            tokenizer = AutoTokenizer.from_pretrained(cfg["path"])
            model = AutoModelForCausalLM.from_pretrained(cfg["path"])
            model = pipeline(cfg["pipeline"], model=model, tokenizer=tokenizer)
        elif cfg["source"] == "api":
            print(f"🌐 Using API endpoint for task {task}")
            model = cfg["endpoint"]  # Will be handled in inference.py
        else:
            raise ValueError(f"Unknown model source: {cfg['source']}")

        self.models[task] = model
        return model

# Singleton loader instance
model_loader = ModelLoader()

