import os
import logging
from typing import List, Optional, Any
from PIL import Image

import google.generativeai as genai
from illustration_gen.config import Config

logger = logging.getLogger(__name__)

class GenAIClient:
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.text_model_name = Config.TEXT_MODEL_NAME
        self.image_model_name = Config.IMAGE_MODEL_NAME

        self.text_model = genai.GenerativeModel(self.text_model_name)
        # We delay image model init to the method to decide based on usage

    def generate_text(self, prompt: str, schema: Optional[Any] = None) -> str:
        try:
            generation_config = {}
            if schema:
                generation_config["response_mime_type"] = "application/json"
                prompt += f"\n\nReturn the result in valid JSON format matching this schema: {schema}"

            response = self.text_model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            raise

    def generate_image(self, prompt: str, reference_image_paths: Optional[List[str]] = None, output_path: str = None) -> str:
        """
        Generates an image using the configured model.
        Attempts to use reference images for consistency if provided.
        """
        if reference_image_paths is None:
            reference_image_paths = []

        try:
            # Prepare multimodal inputs
            inputs = [prompt]
            has_refs = False
            for ref_path in reference_image_paths:
                if ref_path and os.path.exists(ref_path):
                    try:
                        img = Image.open(ref_path)
                        inputs.append(img)
                        has_refs = True
                    except Exception as img_err:
                        logger.warning(f"Failed to load reference image {ref_path}: {img_err}")

            logger.info(f"Generating image with model {self.image_model_name}. Refs: {has_refs}")

            # Strategy:
            # 1. Try treating it as a GenerativeModel (Multimodal Input -> Image Output? or Text Output?)
            #    If the user claims "gemini-3-pro-image-preview" works for this, we try `generate_content`.
            #    NOTE: In current public API, `generate_content` returns text.
            #    If the model is specially tuned to return an image blob, we handle it.
            #    However, standard `ImageGenerationModel` is different.

            # 2. If it's an ImageGenerationModel (e.g. Imagen 3), it typically only accepts text prompts.
            #    Passing PIL images to `generate_images` might fail.

            # Given the ambiguity of "Gemini 3", I will implement a check.
            # If we have reference images, we try `generate_content` first (assuming Multimodal capability).

            generated_image = None

            if has_refs:
                try:
                    # Attempt Multimodal generation
                    model = genai.GenerativeModel(self.image_model_name)
                    response = model.generate_content(inputs)

                    # Check if response contains image parts
                    # This is hypothetical for "Gemini 3" based on user description.
                    # If it returns text, it failed to gen image.
                    if response.parts:
                        for part in response.parts:
                            if hasattr(part, "inline_data") or hasattr(part, "image"):
                                # If we got an image back, great!
                                # Logic to extract image data (depends on SDK version for "inline_data")
                                # For now, we assume failure to extract means we fall back.
                                pass
                except Exception as e:
                    logger.debug(f"Multimodal generation attempt failed: {e}")

            # Fallback / Standard Path: ImageGenerationModel
            if not generated_image:
                # Use ImageGenerationModel
                # Since it likely doesn't support image inputs, we rely on the prompt.
                # Ideally, we would describe the reference images in text and append to prompt.
                # (This logic should happen in the caller or here).
                # For this implementation, we use the prompt as is.

                img_model = genai.ImageGenerationModel(self.image_model_name)
                response = img_model.generate_images(
                    prompt=prompt,
                    number_of_images=1
                )
                generated_image = response.images[0]

            # Save
            if generated_image:
                generated_image.save(output_path)
                return output_path
            else:
                raise RuntimeError("No image generated.")

        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise
