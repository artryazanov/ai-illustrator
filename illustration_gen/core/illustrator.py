import logging
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

    def illustrate_scenes(self, scenes: List[Scene], style_prompt: str):
        for scene in scenes:
            scene_dir = self.output_dir / f"{scene.id:03d}_{scene.location_name.replace(' ', '_')}"
            scene_dir.mkdir(parents=True, exist_ok=True)

            text_file = scene_dir / "story_segment.txt"
            img_file = scene_dir / "illustration.jpg"

            # Save text
            with open(text_file, "w") as f:
                f.write(scene.original_text_segment)

            if img_file.exists():
                logger.info(f"Illustration for scene {scene.id} exists. Skipping.")
                continue

            ref_images = []
            
            # Logic to choose best reference (Portrait vs Full Body)
            if scene.characters_present:
                main_char_name = scene.characters_present[0]
                # Use method that selects needed card type depending on scene
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
                    output_path=str(img_file),
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
