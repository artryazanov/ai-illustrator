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
        
        self.catalog_path = self.char_dir / "characters.json"
        self._load_catalog()

    def _load_catalog(self):
        """Loads character catalog from JSON."""
        if self.catalog_path.exists():
            try:
                with open(self.catalog_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        char = Character(
                            name=item['original_name'],
                            description=item['description'],
                            reference_image_path=item['reference_image_path']
                        )
                        self.characters[char.name] = char
                logger.info(f"Loaded {len(self.characters)} characters from catalog.")
            except Exception as e:
                logger.error(f"Error loading catalog: {e}")

    def _save_catalog(self):
        """Saves current character catalog to JSON."""
        catalog_data = []
        for name, char in self.characters.items():
            folder_name = Path(char.reference_image_path).parent.name if char.reference_image_path else ""
            catalog_data.append({
                "original_name": name,
                "folder_name": folder_name,
                "description": char.description,
                "reference_image_path": char.reference_image_path
            })
        
        try:
            with open(self.catalog_path, "w", encoding="utf-8") as f:
                json.dump(catalog_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
             logger.error(f"Error saving catalog: {e}")

    def generate_character_assets(self, characters: List[Character], style_prompt: str):
        for char in characters:
            # 1. Check catalog first
            if char.name in self.characters:
                logger.info(f"Character {char.name} found in catalog. Using existing asset.")
                # Ensure the passed character object gets the path from the catalog
                char.reference_image_path = self.characters[char.name].reference_image_path
                continue

            # 2. Translate name for folder
            english_name = self.ai_client.translate_to_english(char.name)
            safe_name = "".join(x for x in english_name if x.isalnum() or x in (' ', '_', '-')).strip().replace(' ', '_')
            
            char_path = self.char_dir / safe_name
            char_path.mkdir(parents=True, exist_ok=True)

            desc_file = char_path / "description.txt"
            img_file = char_path / "ref_01.jpg"

            # 3. Check for physical existence (legacy/manual restore)
            if img_file.exists():
                logger.info(f"Asset file for {char.name} already exists at {img_file}. Updating catalog.")
                char.reference_image_path = str(img_file)
                self.characters[char.name] = char
                self._save_catalog()
                continue
            
            # 4. Generate
            with open(desc_file, "w", encoding="utf-8") as f:
                f.write(char.description)

            # Prompt Pattern: "Character sheet of {name}, {description}. {system_style_prompt}. White background, full body shot, neutral expression, flat lighting."
            prompt = f"Character sheet of {char.name}, {char.description}. {style_prompt}. White background, full body shot, neutral expression, flat lighting."
            
            logger.info(f"Generating reference for character: {char.name} (Folder: {safe_name})")
            try:
                self.ai_client.generate_image(prompt=prompt, output_path=str(img_file))
                char.reference_image_path = str(img_file)
                
                # Update catalog
                self.characters[char.name] = char
                self._save_catalog()
                
            except Exception as e:
                logger.error(f"Failed to generate asset for {char.name}: {e}")

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
        if name in self.characters:
            return self.characters[name].reference_image_path
        
        # Fallback to fuzzy
        for key, char in self.characters.items():
            if name in key or key in name:
                return char.reference_image_path
        return None

    def get_location_ref(self, name: str) -> str:
        for key, loc in self.locations.items():
            if name in key or key in name:
                return loc.reference_image_path
        return None
