import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Models as requested by user
    TEXT_MODEL_NAME = os.getenv("TEXT_MODEL_NAME", "gemini-3-pro-preview")
    IMAGE_MODEL_NAME = os.getenv("IMAGE_MODEL_NAME", "gemini-3-pro-image-preview")

    # Fallback to known working models if the preview ones are hypothetical for this environment
    # Note: Logic to switch can be added here if needed, but we stick to requirements.

    BASE_OUTPUT_DIR = Path("output")

    # Generation settings
    DEFAULT_IMAGE_SIZE = (1024, 1024)

    # Global Style Modifiers
    DIGITAL_FIX = (
        "direct digital render, high-quality digital art, clean edges, no paper texture, "
        "no camera grain, no desk, no hands, no glare, no blur, sharp focus."
    )

    @staticmethod
    def validate():
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Ensure output directories exist structure
def setup_directories(base_path: Path):
    dirs = [
        base_path / "characters",
        base_path / "locations",
        base_path / "illustrations"
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
