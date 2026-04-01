import logging
import json
import os
from pathlib import Path
from typing import List, Optional
import concurrent.futures

from app.core.ai_client import GenAIClient
from app.core.asset_manager import AssetManager
from app.core.models import Scene
from app.config import Config

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
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(self._process_single_scene, scene, style_prompt) for scene in scenes]
            concurrent.futures.wait(futures)

        # Save global manifest after processing all scenes
        self._save_data_json(style_prompt)

    def _process_single_scene(self, scene: Scene, style_prompt: str):
        # 1. Generate filename slug
        slug = self.ai_client.generate_filename_slug(scene.visual_description or scene.summary)
        filename = f"{scene.id}_{slug}.jpeg"
        
        img_file = self.output_dir / filename

        # 2. Collect location info
        loc_data = self.asset_manager.get_location_data(scene.location_name)
        location_info = {
            "id": getattr(loc_data, 'id', None),
            "name": scene.location_name
        }

        # 3. Collect character info
        characters_info = []
        for char_name in scene.characters_present:
            char_data = self.asset_manager.get_character_data(char_name)
            if char_data:
                characters_info.append({
                    "id": getattr(char_data, 'id', None),
                    "name": char_name,
                    "full_body_path": getattr(char_data, 'full_body_path', None)
                })

        # 4. Save Scene JSON Metadata
        scene_metadata = {
            "scene_id": scene.id,
            "story_segment": scene.original_text_segment,
            "name": slug,
            "location": location_info,
            "characters": characters_info,
            "illustration_path": str(img_file.relative_to(self.output_dir.parent)),
            "generation_prompt": None
        }
        
        self.illustrations_registry.append(scene_metadata)

        if img_file.exists():
            logger.info(f"Illustration for scene {scene.id} exists. Skipping generation.")
            return

        logger.info(f"Analyzing scene {scene.id} for highlight moment...")
        highlight_data = self.ai_client.analyze_scene_for_highlight(
            scene.original_text_segment, 
            available_characters=scene.characters_present
        )
        highlight_prompt = highlight_data.get("image_prompt")
        active_characters = highlight_data.get("active_characters")

        prompt = self._generate_scene_image(scene, style_prompt, img_file, highlight_prompt, active_characters)
        if prompt:
            scene_metadata["generation_prompt"] = prompt

    def _save_data_json(self, style_prompt: str):
        """Creates a global JSON manifest with all illustrations, style, characters, and locations."""
        manifest_path = self.output_dir.parent / "data.json"
        ordered_list = sorted(self.illustrations_registry, key=lambda x: x['scene_id'])
        
        # Collect character data for export
        char_list = []
        for name, char in self.asset_manager.characters.items():
            c_data = {
                "id": char.id,
                "original_name": char.original_name or name,
                "name": char.name,
                "description": char.description,
                "reference_image_path": char.reference_image_path,
                "full_body_path": char.full_body_path,
                "generation_prompt": char.generation_prompt
            }
            char_list.append(c_data)

        # Collect location data for export
        loc_list = []
        for name, loc in self.asset_manager.locations.items():
            loc_list.append({
                "id": loc.id,
                "original_name": loc.original_name or name,
                "name": loc.name,
                "description": loc.description,
                "reference_image_path": loc.reference_image_path,
                "generation_prompt": loc.generation_prompt
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

    def _generate_scene_image(self, scene: Scene, style_prompt: str, output_path: Path, highlight_prompt: Optional[str] = None, active_characters: Optional[List[str]] = None) -> Optional[str]:
        reference_images = []
        anchors_text_blocks = []
        
        # Determine who is actually present in the frame
        chars_to_include = active_characters if active_characters is not None else scene.characters_present
        
        # 1. Collect data for ALL scene characters (Text + Image)
        for char_name in chars_to_include:
            char_data = self.asset_manager.get_character_data(char_name)
            if char_data:
                # Add textual anchor
                anchors_text_blocks.append(f"[CHARACTER '{char_name}']: {char_data.description}")
                
                # Attach visual reference
                ref_path = self._select_character_ref(char_name, scene)
                if ref_path:
                    reference_images.append({
                        "path": ref_path,
                        "purpose": f"Character Appearance Reference for {char_name}",
                        "usage": f"Strictly maintain the facial features, clothing, and body type of {char_name} exactly as shown in this image."
                    })

        # 2. Collect location data (Text + Image)
        loc_data = self.asset_manager.get_location_data(scene.location_name)
        if loc_data:
            anchors_text_blocks.append(f"[LOCATION '{scene.location_name}']: {loc_data.description}")
            
        loc_ref = self.asset_manager.get_location_ref(scene.location_name)
        if loc_ref:
            reference_images.append({
                "path": loc_ref,
                "purpose": f"Environment Reference for {scene.location_name}",
                "usage": "Use this as the absolute source of truth for the background, architecture, and environmental lighting."
            })

        # Form final text blocks
        anchors_text = "\n".join(anchors_text_blocks)
        visual_core = highlight_prompt if highlight_prompt else scene.visual_description

        validation_rules = """
        1. Single Frame Rule: The image MUST be a single cinematic shot. NO split screens, NO comic book panels, NO grid layouts, NO borders.
        2. No Text Rule: The image MUST contain NO text, NO watermarks, NO speech bubbles, and NO UI elements.
        """

        # 4. Form structured prompt with strong context
        base_prompt = (
            f"{style_prompt}. **Single cinematic frame. One single cohesive image.**\n"
            f"**Follow the visual style of the attached reference images precisely.**\n"
            f"**STRICTLY NO multi-panels, NO comic book layout, NO grid, NO split screen.**\n"
            f"**NO text, NO captions, NO speech bubbles.**\n\n"
            f"--- MANDATORY VISUAL DETAILS ---\n"
            f"You MUST faithfully represent the following entities in the scene using these exact descriptions:\n"
            f"{anchors_text}\n"
            f"--------------------------------\n\n"
            f"Scene context: {visual_core}\n"
            f"Action taking place: {scene.action_description}\n"
            f"Setting: {scene.location_name}, {scene.time_of_day}. Mood: {scene.mood}."
        )

        attempt = 1
        feedback = None
        is_valid = False

        while attempt <= Config.MAX_RETRIES:
            logger.info(f"Generating illustration for Scene {scene.id} with {len(reference_images)} refs (Attempt {attempt}/{Config.MAX_RETRIES})...")
            
            current_prompt = base_prompt + f"\n{Config.DIGITAL_FIX}"
            if feedback:
                safe_feedback = self.ai_client.sanitize_prompt_feedback(feedback)
                current_prompt += (
                    f"\n\n[CRITICAL CORRECTION REQUIRED]\n{safe_feedback}. "
                    f"IMPORTANT: While applying the correction, you MUST strictly maintain the exact character identity, "
                    f"clothing, and face from the provided reference images. Do not invent a new character or change the style!"
                )

            try:
                self.ai_client.generate_image(
                    prompt=current_prompt,
                    reference_images=reference_images,
                    output_path=str(output_path),
                    aspect_ratio=Config.IMAGE_ASPECT_RATIO
                )
                
                qa_result = self.ai_client.validate_image(
                    generated_image_path=str(output_path),
                    validation_rules=validation_rules,
                    reference_images=[]
                )

                if qa_result.is_valid:
                    logger.info(f"✅ Scene {scene.id} passed QA validation!")
                    is_valid = True
                    return current_prompt
                else:
                    logger.warning(f"❌ Scene {scene.id} validation failed: {qa_result.feedback}")
                    feedback = qa_result.feedback
                    attempt += 1

            except Exception as e:
                logger.error(f"Failed to illustrate scene {scene.id} on attempt {attempt}: {e}")
                attempt += 1

        if not is_valid:
             logger.warning(f"⚠️ Max retries reached for Scene {scene.id}. Proceeding with the last generated image.")
        
        return current_prompt

    def _select_character_ref(self, char_name: str, scene: Scene) -> Optional[str]:
        """Selects character reference (always full body now)."""
        char_data = self.asset_manager.get_character_data(char_name)
        if not char_data:
            return None
            
        return char_data.full_body_path or char_data.reference_image_path
