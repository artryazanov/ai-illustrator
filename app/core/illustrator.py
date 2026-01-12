import logging
import json
import os
from pathlib import Path
from typing import List, Optional

from app.core.ai_client import GenAIClient
from app.core.asset_manager import AssetManager
from app.core.models import Scene

logger = logging.getLogger(__name__)


class StoryIllustrator:
    def __init__(self, ai_client: GenAIClient, asset_manager: AssetManager, output_dir: Path):
        self.ai_client = ai_client
        self.asset_manager = asset_manager
        self.output_dir = output_dir / "illustrations"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Registry for all generated illustrations
        self.illustrations_registry = []

    def illustrate_scenes(self, scenes: List[Scene], style_prompt: str):
        for scene in scenes:
            scene_folder_name = f"{scene.id:03d}_{scene.location_name.replace(' ', '_')}"
            scene_dir = self.output_dir / scene_folder_name
            scene_dir.mkdir(parents=True, exist_ok=True)

            img_file = scene_dir / "illustration.jpg"

            # 1. Collect location info
            # Using get_location_ref but we really want the full object if possible for paths
            # The asset_manager.locations dict should have it if generated
            loc_data = self.asset_manager.locations.get(scene.location_name)
            location_info = {
                "name": scene.location_name,
                "path": loc_data.reference_image_path if loc_data else None
            }

            # 2. Collect character info
            characters_info = []
            for char_name in scene.characters_present:
                # Try to find character data using fuzzy matching helper
                char_data = self.asset_manager.get_character_data(char_name)
                if char_data:
                    characters_info.append({
                        "name": char_name,
                        "portrait_path": getattr(char_data, 'portrait_path', None),
                        "full_body_path": getattr(char_data, 'full_body_path', None)
                    })

            # 3. Save Scene JSON
            scene_metadata = {
                "scene_id": scene.id,
                "story_segment": scene.original_text_segment,
                "location": location_info,
                "characters": characters_info,
                "illustration_path": str(img_file.relative_to(self.output_dir.parent)),
                "folder": scene_folder_name
            }
            
            # Add to global registry
            self.illustrations_registry.append(scene_metadata)

            if img_file.exists():
                logger.info(f"Illustration for scene {scene.id} exists. Skipping generation.")
                continue

            self._generate_scene_image(scene, style_prompt, img_file)

        # Save global manifest after processing all scenes
        self._save_data_json(style_prompt)

    def _save_data_json(self, style_prompt: str):
        """Creates a global JSON manifest with all illustrations, style, characters, and locations."""
        manifest_path = self.output_dir.parent / "data.json"
        ordered_list = sorted(self.illustrations_registry, key=lambda x: x['scene_id'])
        
        # Collect character data for export
        char_list = []
        for name, char in self.asset_manager.characters.items():
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

        # Collect location data for export
        loc_list = []
        for name, loc in self.asset_manager.locations.items():
            loc_list.append({
                "original_name": loc.original_name or name,
                "name": loc.name,
                "description": loc.description,
                "reference_image_path": loc.reference_image_path
            })

        data = {
            "style_prompt": style_prompt,
            "characters": char_list,
            "locations": loc_list,
            "illustrations": ordered_list
        }
        
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Global manifest saved to {manifest_path}")

    def _generate_scene_image(self, scene: Scene, style_prompt: str, output_path: Path):
        reference_images = []
        
        if scene.characters_present:
            main_char_name = scene.characters_present[0]
            ref_path = self._select_character_ref(main_char_name, scene)
            if ref_path:
                reference_images.append({
                    "path": ref_path,
                    "purpose": f"Character Appearance Reference for {main_char_name}",
                    "usage": "Maintain consistency with this character design."
                })

        # Add location reference (16:9)
        loc_ref = self.asset_manager.get_location_ref(scene.location_name)
        if loc_ref:
            reference_images.append({
                "path": loc_ref,
                "purpose": "Location Environment Reference",
                "usage": "Set the scene in this environment."
            })

        # Enhanced prompt to prevent comic layout
        prompt = (
            f"{style_prompt}. **Single cinematic frame. One single cohesive image.**\n"
            f"**STRICTLY NO multi-panels, NO comic book layout, NO grid, NO split screen, NO storyboard, NO frames.**\n"
            f"**NO text, NO captions, NO speech bubbles.**\n"
            f"Scene context: {scene.visual_description}\n"
            f"Action taking place: {scene.action_description}\n"
            f"Setting: {scene.location_name}, {scene.time_of_day}. Mood: {scene.mood}."
        )

        logger.info(f"Generating illustration for Scene {scene.id} (Single Frame)...")
        try:
            self.ai_client.generate_image(
                prompt=prompt,
                reference_images=reference_images,
                output_path=str(output_path),
                aspect_ratio="16:9"
            )
        except Exception as e:
            logger.error(f"Failed to illustrate scene {scene.id}: {e}")

    def _select_character_ref(self, char_name: str, scene: Scene) -> Optional[str]:
        """Selects character reference (always full body now)."""
        char_data = self.asset_manager.get_character_data(char_name)
        if not char_data:
            return None
            
        return char_data.full_body_path or char_data.reference_image_path
