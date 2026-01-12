import os
import json
import logging
from pathlib import Path
from typing import List, Dict

from illustration_gen.config import Config
from illustration_gen.core.ai_client import GenAIClient
from illustration_gen.core.models import Character, Location

logger = logging.getLogger(__name__)

class AssetManager:
    def __init__(self, ai_client: GenAIClient, output_dir: Path):
        self.ai_client = ai_client
        self.output_dir = output_dir
        self.char_dir = output_dir / "characters"
        self.loc_dir = output_dir / "locations"

        # In-memory registry to avoid re-generating in same run
        self.characters: Dict[str, Character] = {}
        self.locations: Dict[str, Location] = {}

    def generate_character_assets(self, characters: List[Character], style_prompt: str):
        for char in characters:
            safe_name = "".join(x for x in char.name if x.isalnum() or x in (' ', '_', '-')).strip().replace(' ', '_')
            char_path = self.char_dir / safe_name
            char_path.mkdir(parents=True, exist_ok=True)

            desc_file = char_path / "description.txt"
            img_file = char_path / "ref_01.jpg" # Using jpg as requested or png

            # Check if exists
            if img_file.exists():
                logger.info(f"Asset for character {char.name} already exists. Skipping.")
                char.reference_image_path = str(img_file)
                self.characters[char.name] = char
                continue

            # Save description
            with open(desc_file, "w") as f:
                f.write(char.description)

            # Generate Reference Image
            # Prompt Pattern: "Character sheet of {name}, {description}. {system_style_prompt}. White background, full body shot, neutral expression, flat lighting."
            prompt = f"Character sheet of {char.name}, {char.description}. {style_prompt}. White background, full body shot, neutral expression, flat lighting."
            
            logger.info(f"Generating reference for character: {char.name}")
            try:
                # We do NOT use reference images here (it's the first gen). 
                self.ai_client.generate_image(prompt=prompt, output_path=str(img_file))
                char.reference_image_path = str(img_file)
            except Exception as e:
                logger.error(f"Failed to generate asset for {char.name}: {e}")

            self.characters[char.name] = char

    def generate_location_assets(self, locations: List[Location], style_prompt: str):
        for loc in locations:
            safe_name = "".join(x for x in loc.name if x.isalnum() or x in (' ', '_', '-')).strip().replace(' ', '_')
            loc_path = self.loc_dir / safe_name
            loc_path.mkdir(parents=True, exist_ok=True)

            desc_file = loc_path / "description.txt"
            img_file = loc_path / "ref_01.jpg"

            if img_file.exists():
                logger.info(f"Asset for location {loc.name} already exists. Skipping.")
                loc.reference_image_path = str(img_file)
                self.locations[loc.name] = loc
                continue

            with open(desc_file, "w") as f:
                f.write(loc.description)

            # Prompt Pattern: "Concept art of {location_name}, {location_description}. {system_style_prompt}. Wide angle, establishing shot."
            prompt = f"Concept art of {loc.name}, {loc.description}. {style_prompt}. Wide angle, establishing shot."

            logger.info(f"Generating reference for location: {loc.name}")
            try:
                self.ai_client.generate_image(prompt=prompt, output_path=str(img_file))
                loc.reference_image_path = str(img_file)
            except Exception as e:
                logger.error(f"Failed to generate asset for {loc.name}: {e}")

            self.locations[loc.name] = loc

    def get_character_ref(self, name: str) -> str:
        # Simple fuzzy match or exact match
        for key, char in self.characters.items():
            if name in key or key in name:
                return char.reference_image_path
        return None

    def get_location_ref(self, name: str) -> str:
        for key, loc in self.locations.items():
            if name in key or key in name:
                return loc.reference_image_path
        return None
