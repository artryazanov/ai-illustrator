from google import genai
from google.genai import types
import logging
from typing import List, Optional, Any, Dict
from PIL import Image
from app.config import Config
import json
import os

logger = logging.getLogger(__name__)

class GenAIClient:
    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.text_model_name = Config.TEXT_MODEL_NAME
        self.image_model_name = Config.IMAGE_MODEL_NAME

    def generate_text(self, prompt: str, schema: Optional[Any] = None) -> str:
        try:
            config_args = {}
            if schema:
                config_args['response_mime_type'] = 'application/json'
                config_args['response_schema'] = schema

            response = self.client.models.generate_content(
                model=self.text_model_name,
                contents=prompt,
                config=config_args
            )
            
            # If we return based on schema, it might be a structured object or text JSON.
            # The SDK might return a parsed object if response_schema is set and SDK handles it.
            # But usually response.text contains the JSON string.
            # If using Pydantic schema, 'response.parsed' might be available in newer SDKs, 
            # otherwise we stick to response.text for broad compatibility unless we verify SDK version.
            # We'll return text and let caller parse or handled parsed if available.
            
            return response.text
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise

    def translate_to_english(self, text: str) -> str:
        """Translates text to English for folder naming."""
        try:
            prompt = f"Translate the following name or phrase to English, providing only the translation, no extra text or punctuation: {text}"
            return self.generate_text(prompt).strip().replace(" ", "_")
        except Exception as e:
            logger.warning(f"Translation failed for '{text}': {e}. Using original name.")
            return text

    def generate_filename_slug(self, text: str) -> str:
        """Generates a short, snake_case filename slug from a description."""
        try:
            prompt = (
                f"Create a short, concise filename slug (max 4 words, snake_case) that summarizes this scene. "
                f"Return ONLY the slug, no extension, no other text. Input: {text}"
            )
            slug = self.generate_text(prompt).strip().lower()
            # Basic sanitization
            slug = "".join(x for x in slug if x.isalnum() or x == '_')
            return slug
        except Exception as e:
            logger.warning(f"Slug generation failed: {e}. Using fallback.")
            return "scene"

    def analyze_scene_for_highlight(self, scene_text: str, available_characters: List[str] = None) -> Dict[str, Any]:
        """
        Analyzes the scene text to identify the most visually striking and significant moment
        for illustration, avoiding temporal inconsistencies of long scenes.
        
        Args:
            scene_text: The text of the scene to analyze.
            available_characters: List of character names known to be in the scene.
            
        Returns:
            dict: {
                "highlight_description": "Description of the specific moment",
                "image_prompt": "Detailed image generation prompt for this moment",
                "active_characters": ["Char1", "Char2"] # Subset of available_characters present in the highlight
            }
        """
        char_context = ""
        if available_characters:
            char_list_str = ", ".join(available_characters)
            char_context = (
                f"The following characters are present in the full scene: {char_list_str}.\n"
                "Identify EXACTLY which of these characters are visible in the specific highlight moment you chose. "
                "Only list characters that are visually present in this split-second."
            )

        try:
            prompt = (
                "Analyze the following scene text. This scene might cover a period of time with multiple actions.\n"
                "To create a SINGLE cohesive illustration, identify the MOST visually striking, dramatic, or significant split-second moment.\n"
                "Ignore everything that happens before or after this specific moment to avoid generated artifacts (like a character doing two things at once).\n\n"
                f"Scene Text: \"{scene_text}\"\n\n"
                f"{char_context}\n\n"
                "Return a JSON object with exactly these keys:\n"
                "- \"highlight_description\": A brief explanation of the chosen moment.\n"
                "- \"image_prompt\": A highly detailed visual description of THIS SPECIFIC MOMENT ONLY. "
                "Describe the subjects, action, lighting, and camera angle. "
                "Do NOT mention that it is a 'highlight' or 'moment', just describe the visual content.\n"
                "- \"active_characters\": A list of strings containing ONLY the names of characters from the provided list that are in this moment."
            )
            
            response_text = self.generate_text(prompt, schema=None) # Start with plain text, relying on model to output JSON
            
            # Clean up potential markdown blocks if the model wraps JSON
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            
            data = json.loads(clean_text)
            
            # Validate active_characters against available_characters if possible
            if available_characters and "active_characters" in data:
                # Filter to ensure we only get known characters, handling potential hallucinations
                valid_chars = [c for c in data["active_characters"] if c in available_characters]
                data["active_characters"] = valid_chars
                
            return data
            
        except Exception as e:
            logger.error(f"Failed to analyze scene highlight: {e}")
            # Fallback
            return {
                "highlight_description": "Fallback: Full scene context",
                "image_prompt": scene_text,
                "active_characters": available_characters or []
            }

    def generate_image(self, prompt: str, reference_images: Optional[List[Dict[str, str]]] = None, output_path: str = None, aspect_ratio: str = "16:9") -> str:
        """
        Generates an image using the configured model. 
        Uses generate_content for multimodal inputs (Subject References) if provided.
        
        Args:
            prompt: The main prompt for image generation.
            reference_images: List of dicts, each containing:
                - path: str (required)
                - purpose: str (optional, e.g. "Character Reference")
                - usage: str (optional, e.g. "Adopt style and appearance")
            output_path: Path to save the generated image.
            aspect_ratio: Aspect ratio for the image.
        """
        if reference_images is None:
            reference_images = []

        try:
            logger.info(f"Generating image with model {self.image_model_name}. Refs: {len(reference_images)}")

            # The user provided docs confirm that 'gemini-3-pro-image-preview' uses 'generate_content'
            # for both text-to-image and multimodal image gen.
            # 'generate_images' is for Imagen or older endpoints, but 'predict' 404s suggest mismatch.
            # We will switch to unified 'generate_content' for everything.
            
            # Construct enhanced prompt with reference context
            final_prompt = prompt
            if reference_images:
                final_prompt += "\n\nReference Images Context:"
                for ref in reference_images:
                    path = ref.get('path')
                    if path:
                        filename = os.path.basename(path)
                        purpose = ref.get('purpose', 'Reference')
                        usage = ref.get('usage', 'Use as visual reference.')
                        final_prompt += f"\n- File: {filename}\n  Purpose: {purpose}\n  Instruction: {usage}"

            contents = [final_prompt]
            if reference_images:
                for ref in reference_images:
                    ref_path = ref.get('path')
                    if ref_path and os.path.exists(ref_path):
                            try:
                                contents.append(Image.open(ref_path))
                            except Exception as img_e:
                                logger.warning(f"Could not load ref image {ref_path}: {img_e}")

            # Config for image generation
            # We must specify response_modalities=['IMAGE'] for image output (or TEXT, IMAGE)
            # Adding aspect_ratio to config
            response = self.client.models.generate_content(
                model=self.image_model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE'],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                    ),
                )
            )
            
            if response.parts:
                for part in response.parts:
                    # Check for image bytes first
                    if hasattr(part, 'image') and part.image:
                         with open(output_path, "wb") as f:
                            f.write(part.image.image_bytes)
                         return output_path
                    
                    # Check for as_image method
                    if hasattr(part, 'as_image'):
                        pil_img = part.as_image()
                        if pil_img:
                            pil_img.save(output_path)
                            return output_path
                            
                    # Check for inline_data
                    if hasattr(part, 'inline_data') and part.inline_data:
                         # This usually needs decoding but SDK might wrap it in 'image' property or as_image
                         pass

            raise RuntimeError("Gemini generation returned no images.")

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise
