import logging
import os
from pathlib import Path
from typing import List

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

            # Gather references
            # Strategy: Focus on Protagonist.
            # We pick the FIRST character in characters_present as the protagonist for this scene
            # (Assuming analyzer orders them by importance or presence).
            
            ref_images = []
            main_char_name = None
            
            if scene.characters_present:
                main_char_name = scene.characters_present[0]
                ref_path = self.asset_manager.get_character_ref(main_char_name)
                if ref_path:
                    ref_images.append(ref_path)
                    logger.info(f"Scene {scene.id}: Using reference for main character '{main_char_name}'")

            # We can also add location ref if available, but "Focus on Protagonist" suggests prioritizing people.
            # However, `ai_client` handles list of refs. If we want to risk it, we add loc.
            # User warning: "Attempts to insert 5 characters... leads to quality drop".
            # 1 Char + 1 Loc might be okay? Let's try just Char for now to be safe, or both if reliable.
            # Let's stick to Char as primary subject per user hint.
            
            # Construct Prompt
            prompt = f"""
            {style_prompt}
            Transformation of: {scene.visual_description}
            Action: {scene.action_description}
            Mood: {scene.mood}
            Time: {scene.time_of_day}
            Location: {scene.location_name}
            """
            
            if main_char_name:
                prompt += f"\nMain Character: {main_char_name} (Reference provided)."
            
            other_chars = [c for c in scene.characters_present if c != main_char_name]
            if other_chars:
                prompt += f"\nOther characters present: {', '.join(other_chars)}."

            logger.info(f"Generating illustration for Scene {scene.id}...")
            try:
                self.ai_client.generate_image(
                    prompt=prompt,
                    reference_image_paths=ref_images,
                    output_path=str(img_file)
                )
            except Exception as e:
                logger.error(f"Failed to illustrate scene {scene.id}: {e}")
