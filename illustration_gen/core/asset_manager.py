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
        
        self.template_dir = output_dir / "style_templates"
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # Global templates
        self.templates = {
            "bg_p": self.template_dir / "bg_portrait.jpg",
            "bg_f": self.template_dir / "bg_fullbody.jpg",
            "ref_p": self.template_dir / "style_reference_portrait.jpg",
            "ref_f": self.template_dir / "style_reference_fullbody.jpg"
        }

        # In-memory registry to avoid re-generating in same run
        self.characters: Dict[str, Character] = {}
        self.locations: Dict[str, Location] = {}
        
        self.catalog_path = self.char_dir / "characters.json"
        self._load_catalog()

    def prepare_style_templates(self, detected_style: str):
        """Creates base backgrounds and style templates once per run."""
        logger.info("Preparing global style templates...")
        
        # 1. Generate clean backgrounds (9:16)
        # Rigidly forbid text and UI
        bg_base_prompt = f"{detected_style}. 9:16 aspect ratio, vertical orientation. Neutral background, no characters, no text, no frames, no interface elements."
        
        if not self.templates["bg_p"].exists():
            self.ai_client.generate_image(f"{bg_base_prompt}. Close-up environment focus.", output_path=str(self.templates["bg_p"]))
        
        if not self.templates["bg_f"].exists():
            self.ai_client.generate_image(f"{bg_base_prompt}. Wide shot environment focus.", output_path=str(self.templates["bg_f"]))

        # 2. Generate 'style reference' characters
        style_ref_prompt = f"A placeholder character to establish art style. {detected_style}. Single character, no text, no split screens, 9:16 aspect ratio."
        
        if not self.templates["ref_p"].exists():
            self.ai_client.generate_image(
                f"{style_ref_prompt}. Portrait shot, head and shoulders.",
                reference_image_paths=[str(self.templates["bg_p"])], # Use our bg
                output_path=str(self.templates["ref_p"])
            )
            
        if not self.templates["ref_f"].exists():
            self.ai_client.generate_image(
                f"{style_ref_prompt}. Full body shot, standing.",
                reference_image_paths=[str(self.templates["bg_f"])], # Use our bg
                output_path=str(self.templates["ref_f"])
            )

    def _load_catalog(self):
        """Loads character catalog from JSON."""
        if self.catalog_path.exists():
            try:
                with open(self.catalog_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        char = Character(
                            name=item.get('name', item['original_name']), # Fallback if needed, but original_name is key
                            description=item['description'],
                            reference_image_path=item.get('reference_image_path'),
                            portrait_path=item.get('portrait_path'),
                            full_body_path=item.get('full_body_path'),
                            original_name=item.get('original_name')
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
                "original_name": char.original_name or name,
                "folder_name": folder_name,
                "description": char.description,
                "reference_image_path": char.reference_image_path,
                "portrait_path": char.portrait_path,
                "full_body_path": char.full_body_path
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
                logger.info(f"Character {char.name} found in catalog. Using existing assets.")
                existing_char = self.characters[char.name]
                char.portrait_path = existing_char.portrait_path
                char.full_body_path = existing_char.full_body_path
                char.reference_image_path = existing_char.reference_image_path or existing_char.full_body_path
                continue

            # 2. Translate name for folder
            english_name = self.ai_client.translate_to_english(char.name)
            safe_name = "".join(x for x in english_name if x.isalnum() or x in (' ', '_', '-')).strip().replace(' ', '_')
            
            char_dir = self.char_dir / safe_name
            char_dir.mkdir(parents=True, exist_ok=True)

            desc_file = char_dir / "description.txt"
            
            # 3. Generate Cards
            with open(desc_file, "w", encoding="utf-8") as f:
                f.write(char.description)

            # Generate Portrait
            self._generate_single_card(char, style_prompt, char_dir, is_full_body=False)
            # Generate Full Body
            self._generate_single_card(char, style_prompt, char_dir, is_full_body=True)
            
            # Set legacy reference path to full body as default
            char.reference_image_path = char.full_body_path
            char.original_name = char.name
            
            # 4. Update Catalog
            self.characters[char.name] = char
            self._save_catalog()

    def _generate_single_card(self, char: Character, style_prompt: str, output_dir: Path, is_full_body: bool):
        suffix = "full" if is_full_body else "port"
        bg_ref = self.templates["bg_f"] if is_full_body else self.templates["bg_p"]
        style_ref = self.templates["ref_f"] if is_full_body else self.templates["ref_p"]
        
        output_file = output_dir / f"card_{suffix}.jpg"
        
        if output_file.exists():
            if is_full_body:
                char.full_body_path = str(output_file)
            else:
                char.portrait_path = str(output_file)
            return

        view_type = "full body shot" if is_full_body else "portrait shot, head and shoulders"
        prompt = (
            f"{view_type} of {char.name}, {char.description}. {style_prompt}. "
            f"9:16 aspect ratio. Single character only. No text, no labels, no frames, "
            f"no UI, no infographics. Exactly one depiction of the character."
        )

        logger.info(f"Generating {suffix} for {char.name}...")
        try:
            self.ai_client.generate_image(
                prompt=prompt,
                reference_image_paths=[str(bg_ref), str(style_ref)],
                output_path=str(output_file)
            )
            if is_full_body:
                char.full_body_path = str(output_file)
            else:
                char.portrait_path = str(output_file)
        except Exception as e:
            logger.error(f"Failed to generate {suffix} for {char.name}: {e}")

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

    def get_character_data(self, name: str) -> Optional[Character]:
        if name in self.characters:
            return self.characters[name]
        
        for key, char in self.characters.items():
            if name in key or key in name:
                return char
        return None

    def get_character_ref(self, name: str) -> str:
        char = self.get_character_data(name)
        return char.reference_image_path if char else None

    def get_location_ref(self, name: str) -> str:
        for key, loc in self.locations.items():
            if name in key or key in name:
                return loc.reference_image_path
        return None
