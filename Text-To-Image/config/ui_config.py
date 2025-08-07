# config/ui_config.py

UI_CONFIG = {
    "moods": [
        "Ethereal", "Cyberpunk", "Melancholy", "Whimsical", "Futuristic",
        "Dreamy", "Dystopian", "Energetic", "Mystical", "Minimalist",
    ],
    "image_types": [
        "Icon", "Logo", "Background", "Sticker", "Vector",
        "Wallpaper", "UI Card", "Product Mockup", "Scene", "Portrait",
    ],
    "art_styles": [
        "Oil Painting", "3D Render", "Pencil Sketch", "Anime", "Pixel Art",
        "Flat Design", "Low Poly", "Realism", "Synthwave", "Pop Art",
    ],
    "frames": [
        "Wide", "Square", "Portrait", "Cinematic", "Isometric",
        "Circle Crop", "Bordered", "No Frame", "Polaroid", "Panorama",
    ],
    "options": {
        "temperature": {
            "min": 0.1,
            "max": 9.5,
            "default": 0.8,
            "step": 0.1
        },
        "num_images": {
            "min": 1,
            "max": 5,
            "default": 1
        },
        "model_select": list(MODEL_OPTIONS.keys())
    }
}
