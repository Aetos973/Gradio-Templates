import os
import joblib
import gradio as gr
from pathlib import Path

# Constants
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "model.pkl"
DATA_DIR = Path("data")
SAMPLE_INPUT_PATH = DATA_DIR / "sample_input.csv"


def load_model():
    """Load the trained model from disk."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading the model: {e}")


def predict(model, input_text):
    """Run model prediction."""
    try:
        prediction = model.predict([input_text])
        return prediction[0]
    except Exception as e:
        return f"Prediction failed: {e}"


def create_interface(model):
    """Create Gradio interface for the model."""
    return gr.Interface(
        fn=lambda x: predict(model, x),
        inputs=gr.Textbox(lines=2, placeholder="Enter text here..."),
        outputs="text",
        title="🧠 AI Model Predictor",
        description="Enter a sentence or phrase, and get a model prediction.",
    )


if __name__ == "__main__":
    try:
        model = load_model()
        demo = create_interface(model)
        demo.launch()
    except Exception as e:
        print(f"[ERROR] Failed to launch app: {e}")
