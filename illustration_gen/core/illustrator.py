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
            ref_images = []

            # Character refs
            char_descriptions = []
            for char_name in scene.characters_present:
                ref_path = self.asset_manager.get_character_ref(char_name)
                if ref_path:
                    ref_images.append(ref_path)
                # We also get the description from the asset manager logic if needed,
                # but we'll rely on the visual prompt construction primarily.

            # Location ref
            loc_ref = self.asset_manager.get_location_ref(scene.location_name)
            if loc_ref:
                ref_images.append(loc_ref)

            # Construct Prompt
            # We explicitly mention we are using references if the model supports prompt-logic for it
            prompt = f"""
            {style_prompt}

            Scene Description:
            {scene.visual_description}

            Action: {scene.action_description}
            Time: {scene.time_of_day}
            Location: {scene.location_name}

            Characters present: {', '.join(scene.characters_present)}

            Make sure the characters and location match the reference images provided (if any).
            Create a cohesive, high-quality illustration.
            """

            logger.info(f"Generating illustration for Scene {scene.id}...")
            try:
                self.ai_client.generate_image(
                    prompt=prompt,
                    reference_image_paths=ref_images,
                    output_path=str(img_file)
                )
            except Exception as e:
                logger.error(f"Failed to illustrate scene {scene.id}: {e}")
