import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional

from app.config import Config
from app.core.ai_client import GenAIClient
from app.core.models import Character, Location

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
            "bg_f": self.template_dir / "bg_fullbody.jpg",
            "ref_f": self.template_dir / "style_reference_fullbody.jpg"
        }

        # In-memory registry to avoid re-generating in same run
        self.characters: Dict[str, Character] = {}
        self.locations: Dict[str, Location] = {}
        
        self.loc_templates = {
            "bg_landscape": self.template_dir / "bg_location_16_9.jpg"
        }
        
        self.data_path = self.output_dir.parent / "data.json"
        
        # Load initial data
        self._load_data()

    def prepare_style_templates(self, detected_style: str):
        """Creates base backgrounds and style templates once per run."""
        logger.info("Preparing global style templates...")
        
        # Tech modifier to prevent "photo effect"
        digital_fix = "direct digital render, high-quality digital art, clean edges, no paper texture, no camera grain, no desk, no hands, no glare."
        
        # 1. Generate clean backgrounds (9:16)
        # Rigidly forbid text and UI
        bg_base_prompt = (
            f"Pure digital illustration in {detected_style} style. 9:16 aspect ratio. "
            f"Solid environment background, no characters, no text, no frames. {digital_fix}"
        )
        
        if not self.templates["bg_f"].exists():
            self.ai_client.generate_image(
                f"{bg_base_prompt}. Wide shot environment focus.",
                reference_image_paths=[str(self.loc_templates["bg_landscape"])],
                output_path=str(self.templates["bg_f"]),
                aspect_ratio="9:16"
            )

        # 2. Generate 'style reference' characters
        style_ref_prompt = (
            f"Character design sheet, {detected_style} style. Full digital artwork. "
            f"Single character, no text, no frames, no split screens, {digital_fix}"
        )
        
        if not self.templates["ref_f"].exists():
            self.ai_client.generate_image(
                f"{style_ref_prompt}. Full body shot, standing.",
                reference_image_paths=[str(self.templates["bg_f"])], # Use our bg
                output_path=str(self.templates["ref_f"]),
                aspect_ratio="9:16"
            )

    def prepare_location_templates(self, detected_style: str):
        """Creates base backgrounds and style templates for locations (16:9)."""
        logger.info("Preparing location style templates (16:9)...")
        
        digital_fix = "direct digital render, high-quality digital art, clean edges, no paper texture, no camera grain, no desk, no glare."
        
        # 1. Neutral background (16:9)
        bg_prompt = (
            f"{detected_style}. 16:9 aspect ratio, horizontal orientation. "
            f"Pure digital environment art, empty scenery, no buildings, no people, "
            f"no text, no borders. Cinematic wide shot. {digital_fix}"
        )
        
        if not self.loc_templates["bg_landscape"].exists():
            self.ai_client.generate_image(
                bg_prompt,
                output_path=str(self.loc_templates["bg_landscape"]),
                aspect_ratio="16:9"
            )



    def _load_data(self):
        """Loads characters and locations from data.json if it exists."""
        if self.data_path.exists():
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # Load Characters
                    for item in data.get('characters', []):
                        char = Character(
                            name=item.get('name', item.get('original_name', 'Unknown')),
                            description=item['description'],
                            reference_image_path=item.get('reference_image_path'),
                            portrait_path=item.get('portrait_path'),
                            full_body_path=item.get('full_body_path'),
                            original_name=item.get('original_name')
                        )
                        self.characters[char.name] = char
                        
                    # Load Locations
                    for item in data.get('locations', []):
                        loc = Location(
                            name=item.get('name', item.get('original_name', 'Unknown')),
                            description=item['description'],
                            reference_image_path=item.get('reference_image_path'),
                            original_name=item.get('original_name')
                        )
                        self.locations[loc.name] = loc
                        
                logger.info(f"Loaded {len(self.characters)} characters and {len(self.locations)} locations from data.json.")
            except Exception as e:
                logger.error(f"Error loading data.json: {e}")
        else:
            # Fallback: Migrate legacy data if data.json doesn't exist
            self._migrate_legacy_data()

    def _migrate_legacy_data(self):
        """One-time migration from legacy independent JSON files."""
        migrated = False
        
        # 1. Migrate Characters
        legacy_char_path = self.char_dir / "characters.json"
        if legacy_char_path.exists():
            try:
                with open(legacy_char_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        char = Character(
                            name=item.get('name', item.get('original_name', 'Unknown')),
                            description=item['description'],
                            reference_image_path=item.get('reference_image_path'),
                            portrait_path=item.get('portrait_path'),
                            full_body_path=item.get('full_body_path'),
                            original_name=item.get('original_name')
                        )
                        self.characters[char.name] = char
                migrated = True
                logger.info(f"Migrated {len(self.characters)} characters from legacy storage.")
            except Exception as e:
                logger.error(f"Error migrating characters: {e}")

        # 2. Migrate Locations
        legacy_loc_path = self.loc_dir / "locations.json"
        if legacy_loc_path.exists():
            try:
                with open(legacy_loc_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        loc = Location(
                            name=item.get('name', item.get('original_name', 'Unknown')),
                            description=item['description'],
                            reference_image_path=item.get('reference_image_path'),
                            original_name=item.get('original_name')
                        )
                        self.locations[loc.name] = loc
                migrated = True
                logger.info(f"Migrated {len(self.locations)} locations from legacy storage.")
            except Exception as e:
                logger.error(f"Error migrating locations: {e}")

        if migrated:
            self._save_data()

    def _save_data(self):
        """Saves current characters and locations to data.json, preserving other fields."""
        current_data = {}
        if self.data_path.exists():
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    current_data = json.load(f)
                    if not isinstance(current_data, dict):
                        current_data = {}
            except Exception:
                pass
        
        # Update Characters
        char_list = []
        for name, char in self.characters.items():
            folder_name = Path(char.reference_image_path).parent.name if char.reference_image_path else ""
            char_list.append({
                "original_name": char.original_name or name,
                "name": char.name,
                "folder_name": folder_name,
                "description": char.description,
                "reference_image_path": char.reference_image_path,
                "portrait_path": char.portrait_path,
                "full_body_path": char.full_body_path
            })
        current_data['characters'] = char_list
        
        # Update Locations
        loc_list = []
        for name, loc in self.locations.items():
            loc_list.append({
                "original_name": loc.original_name or name,
                "name": loc.name,
                "description": loc.description,
                "reference_image_path": loc.reference_image_path
            })
        current_data['locations'] = loc_list
        
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(current_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
             logger.error(f"Error saving data.json: {e}")

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

            # 3. Generate Cards
            # Generate Full Body
            self._generate_single_card(char, style_prompt, char_dir)
            
            # Set legacy reference path to full body as default
            char.reference_image_path = char.full_body_path
            char.original_name = char.name
            
            # 4. Update Data
            self.characters[char.name] = char
            self._save_data()

    def _generate_single_card(self, char: Character, style_prompt: str, output_dir: Path):
        style_ref = self.templates["ref_f"]
        
        output_file = output_dir / f"card_full.jpg"
        
        if output_file.exists():
            char.full_body_path = str(output_file)
            return

        digital_fix = "direct digital render, high-quality digital art, clean edges, no paper texture, no camera grain."
        view_type = "full body shot"
        prompt = (
            f"{view_type} of {char.name}, {char.description}. {style_prompt}. "
            f"9:16 aspect ratio. Single character only. No text, no labels, no frames, "
            f"no UI, no infographics. Exactly one depiction of the character. {digital_fix}"
        )

        logger.info(f"Generating full body for {char.name}...")
        try:
            self.ai_client.generate_image(
                prompt=prompt,
                reference_image_paths=[str(style_ref)],
                output_path=str(output_file),
                aspect_ratio="9:16"
            )
            char.full_body_path = str(output_file)
        except Exception as e:
            logger.error(f"Failed to generate full body for {char.name}: {e}")

    # _load_location_catalog and _save_location_catalog removed in favor of unified _load_data/_save_data

    def generate_location_assets(self, locations: List[Location], style_prompt: str):
        for loc in locations:
            # Check catalog first
            if loc.name in self.locations:
                continue

            # Translate name for folder
            english_name = self.ai_client.translate_to_english(loc.name)
            safe_name = "".join(x for x in english_name if x.isalnum() or x in (' ', '_', '-')).strip().replace(' ', '_')
            
            loc_path = self.loc_dir / safe_name
            loc_path.mkdir(parents=True, exist_ok=True)
            
            img_file = loc_path / "ref_01.jpg"
            
            # 16:9 Prompt
            digital_fix = "direct digital render, high-quality digital art, clean edges, no paper texture, no camera grain."
            prompt = (
                f"Digital landscape art of {loc.name}, {loc.description}. {style_prompt}. "
                f"16:9 aspect ratio, cinematic wide shot. "
                f"Single view, no text, no labels, no split screen, no frames. "
                f"High quality environment design. {digital_fix}"
            )

            try:
                self.ai_client.generate_image(
                    prompt=prompt,
                    reference_image_paths=[
                        str(self.loc_templates["bg_landscape"])
                    ],
                    output_path=str(img_file),
                    aspect_ratio="16:9"
                )
                loc.reference_image_path = str(img_file)
                if not loc.original_name:
                    loc.original_name = loc.name
                
                self.locations[loc.name] = loc
                self._save_data()
                
            except Exception as e:
                logger.error(f"Failed to generate location {loc.name}: {e}")

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
