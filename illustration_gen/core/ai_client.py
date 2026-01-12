from google import genai
from google.genai import types
import logging
from typing import List, Optional, Any, Dict
from PIL import Image
from illustration_gen.config import Config
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

    def generate_image(self, prompt: str, reference_image_paths: Optional[List[str]] = None, output_path: str = None, aspect_ratio: str = "16:9") -> str:
        """
        Generates an image using the configured model. 
        Uses generate_content for multimodal inputs (Subject References) if provided.
        """
        if reference_image_paths is None:
            reference_image_paths = []

        try:
            logger.info(f"Generating image with model {self.image_model_name}. Refs: {len(reference_image_paths)}")

            # The user provided docs confirm that 'gemini-3-pro-image-preview' uses 'generate_content'
            # for both text-to-image and multimodal image gen.
            # 'generate_images' is for Imagen or older endpoints, but 'predict' 404s suggest mismatch.
            # We will switch to unified 'generate_content' for everything.

            contents = [prompt]
            if reference_image_paths:
                for ref_path in reference_image_paths:
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
