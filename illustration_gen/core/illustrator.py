import logging
import json
import os
from pathlib import Path
from typing import List, Optional

from illustration_gen.core.ai_client import GenAIClient
from illustration_gen.core.asset_manager import AssetManager
from illustration_gen.core.models import Scene

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

            metadata_file = scene_dir / "scene_data.json"
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
                "illustration_path": str(img_file.relative_to(self.output_dir.parent))
            }
            
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(scene_metadata, f, ensure_ascii=False, indent=4)

            # Add to global registry
            self.illustrations_registry.append({
                "scene_id": scene.id,
                "illustration_path": scene_metadata["illustration_path"],
                "folder": scene_folder_name
            })

            if img_file.exists():
                logger.info(f"Illustration for scene {scene.id} exists. Skipping generation.")
                continue

            self._generate_scene_image(scene, style_prompt, img_file)

        # Save global manifest after processing all scenes
        self._save_global_manifest()

    def _save_global_manifest(self):
        """Creates a global JSON manifest with all illustrations in order."""
        manifest_path = self.output_dir.parent / "illustrations_sequence.json"
        ordered_list = sorted(self.illustrations_registry, key=lambda x: x['scene_id'])
        
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(ordered_list, f, ensure_ascii=False, indent=4)
        logger.info(f"Global manifest saved to {manifest_path}")

    def _generate_scene_image(self, scene: Scene, style_prompt: str, output_path: Path):
        ref_images = []
        
        # Logic to choose best reference (Portrait vs Full Body)
        if scene.characters_present:
            main_char_name = scene.characters_present[0]
            ref_path = self._select_character_ref(main_char_name, scene)
            if ref_path:
                ref_images.append(ref_path)

        # Add location reference (16:9)
        loc_ref = self.asset_manager.get_location_ref(scene.location_name)
        if loc_ref:
            ref_images.append(loc_ref)

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
                reference_image_paths=ref_images,
                output_path=str(output_path),
                aspect_ratio="16:9"
            )
        except Exception as e:
            logger.error(f"Failed to illustrate scene {scene.id}: {e}")

    def _select_character_ref(self, char_name: str, scene: Scene) -> Optional[str]:
        """Selects between portrait and full body based on scene description."""
        char_data = self.asset_manager.get_character_data(char_name)
        if not char_data:
            return None
            
        portrait_keywords = ['face', 'eyes', 'smile', 'expression', 'close-up', 'лицо', 'эмоция', 'крупный план']
        scene_desc = (scene.visual_description + " " + scene.action_description).lower()
        
        if any(word in scene_desc for word in portrait_keywords):
            return char_data.portrait_path or char_data.full_body_path
        return char_data.full_body_path or char_data.portrait_path
