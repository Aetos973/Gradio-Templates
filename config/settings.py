# config/settings.py

import os
from pathlib import Path

# Root project path
BASE_DIR = Path(__file__).resolve().parent.parent

class AppConfig:
    """
    Centralized configuration for themes, models, and shared assets.
    """

    # ===============================
    # 🔹 General Settings
    # ===============================
    APP_NAME = "Astral Multimodal AI Studio"
    VERSION = "0.1.0"
    DEBUG = True

    # ===============================
    # 🔹 Paths
    # ===============================
    TEMPLATES_DIR = BASE_DIR / "templates"
    COMMON_DIR = TEMPLATES_DIR / "common"
    THEMES_DIR = COMMON_DIR / "themes"
    WALLPAPERS_DIR = COMMON_DIR / "wallpapers"
    ICONS_DIR = COMMON_DIR / "icons"
    FONTS_DIR = COMMON_DIR / "fonts"

    # ===============================
    # 🔹 Themes
    # ===============================
    THEMES = {
        "classic_dark": THEMES_DIR / "classic_dark.css",
        "classic_light": THEMES_DIR / "classic_light.css",
        "cyberpunk_dark": THEMES_DIR / "cyberpunk_dark.css",
        "cyberpunk_light": THEMES_DIR / "cyberpunk_light.css",
        "glass_dark.css": THEMES_DIR / "glass_dark.css",
        "glass_light.css": THEMES_DIR / "glass_light.css",
        "minimal_dark.css": THEMES_DIR / "minimal_dark.css",
        "minimal_light.css": THEMES_DIR / "minimal_light.css",
        "modern_dark.css": THEMES_DIR / "modern_dark.css",
        "modern_light.css": THEMES_DIR / "modern_light.css",
        "nature_dark.css": THEMES_DIR / "nature_dark.css",
        "nature_light.css": THEMES_DIR / "nature_light.css",
        "neo_dark.css": THEMES_DIR / "neo_dark.css",
        "neo_light.css": THEMES_DIR / "neo_light.css", 
        "pastel_dark.css": THEMES_DIR / "pastel_dark.css",
        "pastel_light.css": THEMES_DIR / "pastel_light.css",
        "terminal_dark.css": THEMES_DIR / "terminal_dark.css",
        "terminal_light.css": THEMES_DIR / "terminal_light.css",
        # add more dynamically later
    }
    DEFAULT_THEME = "classic_dark"

    # ===============================
    # 🔹 Wallpapers
    # ===============================
    WALLPAPERS = {
        "dark": list((WALLPAPERS_DIR / "dark").glob("*.jpg")),
        "light": list((WALLPAPERS_DIR / "light").glob("*.jpg"))
    }
    DEFAULT_WALLPAPER = WALLPAPERS["dark"][0] if WALLPAPERS["dark"] else None

    # ===============================
    # 🔹 Models
    # ===============================
    MODELS = {
        "text_to_text": {
            "default": "gpt-neo",
            "options": ["gpt-neo", "mistral", "llama-2"]
        },
        "text_to_image": {
            "default": "stable-diffusion",
            "options": ["stable-diffusion", "sdxl", "dalle"]
        },
        "audio_to_text": {
            "default": "whisper",
            "options": ["whisper", "deepgram", "assemblyai"]
        }
    }

    # ===============================
    # 🔹 Utility Methods
    # ===============================
    @classmethod
    def get_theme(cls, theme_name=None):
        """
        Returns path to the selected theme CSS file.
        """
        theme = theme_name or cls.DEFAULT_THEME
        return cls.THEMES.get(theme, cls.THEMES[cls.DEFAULT_THEME])

    @classmethod
    def get_wallpapers(cls, mode="dark"):
        """
        Returns available wallpapers for light/dark mode.
        """
        return cls.WALLPAPERS.get(mode, [])

    @classmethod
    def get_model(cls, category, model_name=None):
        """
        Returns default or selected model for a category.
        """
        models = cls.MODELS.get(category, {})
        if not models:
            return None
        return model_name or models["default"]
