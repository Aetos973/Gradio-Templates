"""
inference.py
Handles model inference for different tasks.
Supports text, image, video, and audio based on templates.
"""

from model.loader import model_loader
import requests

class InferenceEngine:
    def __init__(self):
        pass

    def run_inference(self, task: str, input_data, **kwargs):
        """
        Runs inference based on the task.
        task: str - one of "text_to_text", "text_to_image", etc.
        input_data: varies (str, image, audio, etc.)
        kwargs: additional parameters (e.g., prompt settings, generation length, etc.)
        """
        model = model_loader.load_model(task)
        cfg = model_loader.models.get(task)

        # HuggingFace / Local model pipeline
        if callable(model):
            result = model(input_data, **kwargs)
            return result

        # API-based model call
        elif isinstance(model, str):  # API endpoint stored as string
            response = requests.post(
                model,
                json={"input": input_data, "params": kwargs}
            )
            return response.json()

        else:
            raise ValueError(f"Unsupported model type for task {task}")

# Singleton inference instance
inference_engine = InferenceEngine()

