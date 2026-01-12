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
        
        self.data_path = self.output_dir / "data.json"
        
        # Load initial data
        self._load_data()

    def prepare_style_templates(self, detected_style: str):
        """Creates base backgrounds and style templates once per run."""
        logger.info("Preparing global style templates...")
        
        # Tech modifier to prevent "photo effect"
        digital_fix = "direct digital render, high-quality digital art, clean edges, no paper texture, no camera grain, no desk, no hands, no glare."
        
        # 1. Generate clean backgrounds (9:16)
        # Rigidly forbid text and UI
        # 1. Generate clean backgrounds (9:16)
        # Rigidly forbid text and UI
        bg_base_prompt = (
            f"{detected_style}. 9:16 aspect ratio. "
            f"Vertical crop of the environment, no characters, no text. "
            f"The visual style, colors, and lighting MUST be an exact match to the reference image. "
            f"{digital_fix}"
        )
        
        if not self.templates["bg_f"].exists():
            self.ai_client.generate_image(
                bg_base_prompt,
                reference_images=[{
                    "path": str(self.loc_templates["bg_landscape"]),
                    "purpose": "Style Foundation",
                    "usage": "This image is the absolute source of truth for visual style, colors, and brushwork. Inherit everything from it."
                }],
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
                reference_images=[{
                    "path": str(self.templates["bg_f"]),
                    "purpose": "Background Style Reference",
                    "usage": "Ensure consistent background style."
                }],
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
                            id=item.get('id'),
                            name=item.get('name', item.get('original_name', 'Unknown')),
                            description=item['description'],
                            reference_image_path=item.get('reference_image_path'),

                            full_body_path=item.get('full_body_path'),
                            original_name=item.get('original_name'),
                            generation_prompt=item.get('generation_prompt')
                        )
                        self.characters[char.name] = char
                        
                    # Load Locations
                    for item in data.get('locations', []):
                        loc = Location(
                            id=item.get('id'),
                            name=item.get('name', item.get('original_name', 'Unknown')),
                            description=item['description'],
                            reference_image_path=item.get('reference_image_path'),
                            original_name=item.get('original_name'),
                            generation_prompt=item.get('generation_prompt')
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

                            full_body_path=item.get('full_body_path'),
                            original_name=item.get('original_name'),
                            generation_prompt=item.get('generation_prompt')
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
                            original_name=item.get('original_name'),
                            generation_prompt=item.get('generation_prompt')
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
            # folder_name kept for legacy compatibility if needed, but not used in new flow
            char_list.append({
                "id": char.id,
                "original_name": char.original_name or name,
                "name": char.name,
                "description": char.description,
                "reference_image_path": char.reference_image_path,

                "full_body_path": char.full_body_path,
                "generation_prompt": char.generation_prompt
            })
        current_data['characters'] = char_list
        
        # Update Locations
        loc_list = []
        for name, loc in self.locations.items():
            loc_list.append({
                "id": loc.id,
                "original_name": loc.original_name or name,
                "name": loc.name,
                "description": loc.description,
                "reference_image_path": loc.reference_image_path,
                "generation_prompt": loc.generation_prompt
            })
        current_data['locations'] = loc_list
        
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(current_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
             logger.error(f"Error saving data.json: {e}")

    def generate_character_assets(self, characters: List[Character], style_prompt: str):
        # Determine next ID
        existing_ids = [c.id for c in self.characters.values() if c.id is not None]
        next_id = max(existing_ids) + 1 if existing_ids else 1

        for char in characters:
            # 1. Check catalog first (exact match)
            if char.name in self.characters:
                logger.info(f"Character {char.name} found in catalog. Using existing assets.")
                existing_char = self.characters[char.name]
                char.id = existing_char.id
                char.full_body_path = existing_char.full_body_path
                char.reference_image_path = existing_char.reference_image_path or existing_char.full_body_path
                continue

            # 2. Check catalog semantic match (AI check)
            semantic_match = self._check_existing_character_semantic(char)
            if semantic_match:
                logger.info(f"Character {char.name} semantically matches existing {semantic_match.name}. Reusing assets.")
                char.id = semantic_match.id
                char.full_body_path = semantic_match.full_body_path
                char.reference_image_path = semantic_match.reference_image_path or semantic_match.full_body_path
                # We keep the new name for the story, but reuse the visual assets.
                self.characters[char.name] = char # Map new name to existing assets object structure
                continue

            # Assign new ID
            char.id = next_id
            next_id += 1

            # 3. Prepare filename: id_snake_case_name.jpeg
            english_name = self.ai_client.translate_to_english(char.name)
            safe_name = "".join(x for x in english_name if x.isalnum() or x in (' ', '_', '-')).strip().replace(' ', '_').lower()
            filename = f"{char.id}_{safe_name}.jpeg"
            
            # Ensure output directory exists (no subfolders)
            self.char_dir.mkdir(parents=True, exist_ok=True)
            output_file = self.char_dir / filename

            # 4. Generate Cards
            # Generate Full Body directly to final path
            if self._generate_single_card(char, style_prompt, output_file):
                # Set legacy reference path to full body as default
                char.full_body_path = str(output_file)
                char.reference_image_path = char.full_body_path
                char.original_name = char.name
            
            # 5. Update Data
            self.characters[char.name] = char
            self._save_data()

    def _generate_single_card(self, char: Character, style_prompt: str, output_file: Path) -> bool:
        style_ref = self.templates["ref_f"]
        
        if output_file.exists():
            char.full_body_path = str(output_file)
            return True

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
                reference_images=[{
                    "path": str(style_ref),
                    "purpose": "Character Style Reference",
                    "usage": "Adopt the art style, line quality, and coloring."
                }],
                output_path=str(output_file),
                aspect_ratio="9:16"
            )
            char.full_body_path = str(output_file)
            char.generation_prompt = prompt
            return True
        except Exception as e:
            logger.error(f"Failed to generate full body for {char.name}: {e}")
            return False

    def generate_location_assets(self, locations: List[Location], style_prompt: str):
        # Determine next ID
        existing_ids = [l.id for l in self.locations.values() if l.id is not None]
        next_id = max(existing_ids) + 1 if existing_ids else 1

        for loc in locations:
            # 1. Check catalog first (exact match)
            existing_loc = self.get_location_data(loc.name)
            if existing_loc:
                logger.info(f"Location {loc.name} matches existing {existing_loc.name}. Reusing assets.")
                loc.id = existing_loc.id
                loc.reference_image_path = existing_loc.reference_image_path
                loc.generation_prompt = existing_loc.generation_prompt
                continue

            # 2. Check catalog semantic match (AI check)
            semantic_match = self._check_existing_location_semantic(loc)
            if semantic_match:
                logger.info(f"Location {loc.name} semantically matches existing {semantic_match.name}. Reusing assets.")
                loc.id = semantic_match.id
                loc.reference_image_path = semantic_match.reference_image_path
                loc.generation_prompt = semantic_match.generation_prompt
                self.locations[loc.name] = loc 
                continue

            # Assign new ID
            loc.id = next_id
            next_id += 1

            # Translate name for filename
            english_name = self.ai_client.translate_to_english(loc.name)
            safe_name = "".join(x for x in english_name if x.isalnum() or x in (' ', '_', '-')).strip().replace(' ', '_').lower()
            filename = f"{loc.id}_{safe_name}.jpeg"
            
            self.loc_dir.mkdir(parents=True, exist_ok=True)
            img_file = self.loc_dir / filename
            
            # 16:9 Prompt
            digital_fix = "direct digital render, high-quality digital art, clean edges, no paper texture, no camera grain."
            prompt = (
                f"Digital landscape art of {loc.name}, {loc.description}. {style_prompt}. "
                f"16:9 aspect ratio, cinematic wide shot. "
                f"Single view, no text, no labels, no split screen, no frames. "
                f"No people, no characters, no figures, no humans, no living beings. Empty scene, architecture and nature only. "
                f"High quality environment design. {digital_fix}"
            )

            try:
                self.ai_client.generate_image(
                    prompt=prompt,
                    reference_images=[{
                        "path": str(self.loc_templates["bg_landscape"]),
                        "purpose": "Environment Style Template",
                        "usage": "Use as stylistic foundation."
                    }],
                    output_path=str(img_file),
                    aspect_ratio="16:9"
                )
                loc.reference_image_path = str(img_file)
                loc.generation_prompt = prompt
                if not loc.original_name:
                    loc.original_name = loc.name
                
                self.locations[loc.name] = loc
                self._save_data()
                
            except Exception as e:
                logger.error(f"Failed to generate location {loc.name}: {e}")

    def _check_existing_character_semantic(self, new_char: Character) -> Optional[Character]:
        """Uses AI to check if the new character matches any existing character description."""
        if not self.characters:
            return None

        # Build list of existing candidates (unique by ID to avoid dupes in prompt)
        # Use a dict to dedup by ID
        unique_chars = {}
        for c in self.characters.values():
            if c.id is not None and c.id not in unique_chars:
                unique_chars[c.id] = c
        
        if not unique_chars:
            return None

        candidates_text = "\n".join([f"- ID {c.id}: Name='{c.name}', Description='{c.description}'" for c in unique_chars.values()])

        prompt = f"""
        I have a new character from a story and a database of existing characters.
        Determine if the new character is actually the SAME person as one of the existing characters, just referred to by a different name or description style.
        
        New Character:
        Name: "{new_char.name}"
        Description: "{new_char.description}"

        Existing Characters Database:
        {candidates_text}

        Task: Compare the New Character to the database. 
        If there is a CLEAR and UNAMBIGUOUS match (e.g. "Main Hero" vs "The Hero", or similar physical description and role), return the ID of the existing character.
        If it is a new character or you are unsure, return null.
        
        Return ONLY a JSON object: {{"match_id": <int or null>, "reason": "<string>"}}
        """

        try:
            response_text = self.ai_client.generate_text(prompt, schema=None)
            # Cleanup json
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            
            match_id = data.get("match_id")
            if match_id is not None:
                # Find the object with this ID
                for c in unique_chars.values():
                    if c.id == match_id:
                        return c
            return None
        except Exception as e:
            logger.warning(f"Semantic match check failed for character {new_char.name}: {e}")
            return None

    def _check_existing_location_semantic(self, new_loc: Location) -> Optional[Location]:
        """Uses AI to check if the new location matches any existing location description."""
        if not self.locations:
            return None

        unique_locs = {}
        for l in self.locations.values():
            if l.id is not None and l.id not in unique_locs:
                unique_locs[l.id] = l
        
        if not unique_locs:
            return None

        candidates_text = "\n".join([f"- ID {l.id}: Name='{l.name}', Description='{l.description}'" for l in unique_locs.values()])

        prompt = f"""
        I have a new location from a story scene and a database of existing locations.
        Determine if the new location is the SAME place as one of the existing locations.

        New Location:
        Name: "{new_loc.name}"
        Description: "{new_loc.description}"

        Existing Locations Database:
        {candidates_text}

        Task: Compare the New Location to the database.
        If it refers to the same place (e.g. "Kitchen" vs "Old Kitchen", or "Forest edge" vs "Dark Forest" if descriptions align), return the ID.
        If not match, return null.

        Return ONLY a JSON object: {{"match_id": <int or null>, "reason": "<string>"}}
        """

        try:
            response_text = self.ai_client.generate_text(prompt, schema=None)
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            
            match_id = data.get("match_id")
            if match_id is not None:
                for l in unique_locs.values():
                    if l.id == match_id:
                        return l
            return None
        except Exception as e:
            logger.warning(f"Semantic match check failed for location {new_loc.name}: {e}")
            return None

    def get_character_data(self, name: str) -> Optional[Character]:
        if name in self.characters:
            return self.characters[name]
        
        for key, char in self.characters.items():
            if name in key or key in name:
                return char
        return None

    def get_location_data(self, name: str) -> Optional[Location]:
        if name in self.locations:
            return self.locations[name]
        
        for key, loc in self.locations.items():
            if name in key or key in name:
                return loc
        return None

    def get_character_ref(self, name: str) -> str:
        char = self.get_character_data(name)
        return char.reference_image_path if char else None

    def get_location_ref(self, name: str) -> str:
        for key, loc in self.locations.items():
            if name in key or key in name:
                return loc.reference_image_path
        return None
