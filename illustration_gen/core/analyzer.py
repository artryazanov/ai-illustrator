import json
import logging
from typing import List

from illustration_gen.core.ai_client import GenAIClient
from illustration_gen.core.models import Scene, Character, Location

logger = logging.getLogger(__name__)

class StoryAnalyzer:
    def __init__(self, ai_client: GenAIClient):
        self.ai_client = ai_client

    def simple_text_splitter(self, text: str, chunk_size: int = 50000, overlap: int = 1000) -> List[str]:
        """
        Splits text into large chunks (e.g., chapters) to fit within context but large enough for semantic analysis.
        """
        if len(text) <= chunk_size:
            return [text]
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = min(start + chunk_size, text_len)
            
            # Find natural break
            if end < text_len:
                search_start = max(start, end - overlap)
                last_newline = text.rfind('\n', search_start, end)
                if last_newline != -1:
                    end = last_newline + 1
                else:
                    last_space = text.rfind(' ', search_start, end)
                    if last_space != -1:
                        end = last_space + 1
            
            chunk = text[start:end]
            chunks.append(chunk)
            start = end 
            
        return chunks

    def extract_style(self, text_segment: str, user_style_prompt: str = "") -> str:
        """
        Acts as Art Director to extract system style prompt.
        """
        prompt = f"""
        Role: Art Director.
        Analyze the following text from a story and determine the most appropriate visual art style for illustrations.
        Consider the tone, genre, and setting.

        Text sample:
        "{text_segment[:5000]}..."

        User preferences (if any): {user_style_prompt}

        Output a detailed style description string. 
        Focus on medium, lighting, color palette, and mood.
        Example output: "Graphic novel style, high contrast, chiaroscuro lighting, black and white with red accents, sharp ink lines, dramatic shadows, Frank Miller aesthetic, gritty texture."
        """
        return self.ai_client.generate_text(prompt)

    def extract_scenes(self, text: str) -> List[Scene]:
        """
        Splits text into scenes using Semantic Chunking via Gemini.
        """
        # 1. Split potentially large text into "Chapters" or large windows
        chunks = self.simple_text_splitter(text, chunk_size=50000, overlap=1000)

        all_scenes = []
        scene_counter = 1

        for chunk_idx, chunk in enumerate(chunks):
            logger.info(f"Analyzing chunk {chunk_idx + 1}/{len(chunks)} for scenes...")
            
            # 2. Ask AI to split this chunk into Scene objects
            prompt = f"""
            Analyze the following text and split it into logical Scenes.
            A new scene starts when there is a change in:
            1. Time (e.g., day to night, later that day)
            2. Location (e.g., moving from indoors to outdoors)
            3. Major Action (e.g., conversation ends, chase begins)

            Return a List of Scene objects.
            Use semantically accurate start/end indices relative to the provided chunk text.
            """

            try:
                # We expect the client to handle the Pydantic schema logic now
                # We need to define a List[Scene] schema or just Scene if the client handles lists.
                # However, Gemini `response_schema` typically wants a Schema object. 
                # Ideally we pass `list[Scene]`.
                
                # Since we refactored ai_client to accept `schema` and pass it to `response_schema`,
                # we can pass the standard python type hint `list[Scene]`.
                
                response_text = self.ai_client.generate_text(prompt + f"\nText:\n{chunk}", schema=list[Scene])
                
                # Parse logic: The SDK might return the JSON text. We need to parse it.
                # If SDK returned parsed object (unlikely with just .text access in our client), we load json.
                # The text should be a JSON list.
                
                try:
                    data = json.loads(response_text)
                    # If data is a list
                    if isinstance(data, list):
                        sorted_data = sorted(data, key=lambda x: x.get('start_index', 0))
                        for s_data in sorted_data:
                            # Adjust indices if needed or just use as relative
                            # Note: s_data might not fully match Scene if model hallucinated, validation happens here
                            
                            # We might need to map keys if Pydantic didn't enforce 100% (rare with Gemini 1.5/3)
                            # Assuming valid structure
                            scene = Scene(**s_data)
                            
                            # Ensure ID is unique across chunks
                            scene.id = scene_counter 
                            scene_counter += 1
                            
                            # Store the actual text segment if indices are reliable
                            # Or rely on what the model returned if it included 'original_text_segment'
                            
                            all_scenes.append(scene)
                    else:
                        logger.warning("Model returned non-list JSON for scenes.")
                        
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse JSON scene response: {response_text[:100]}...")

            except Exception as e:
                logger.error(f"Failed to extract scenes from chunk: {e}")
                # Fallback?
                pass

        return all_scenes

    def extract_characters(self, text: str) -> List[Character]:
        """
        Extracts Character Sheets (Visual Descriptions).
        """
        prompt = f"""
        Analyze the text and identify key characters.
        Create a Visual Portrait for each.
        Focus on: Hair color/style, Eye color, Clothing, Body type, Age, Distinctive features (scars, glasses).
        Ignore abstract personality traits. Focus ONLY on visual traits.
        """

        try:
            response_text = self.ai_client.generate_text(prompt + f"\nText:\n{text}", schema=list[Character])
            data = json.loads(response_text)
            return [Character(**d) for d in data]
        except Exception as e:
            logger.error(f"Error extracting characters: {e}")
            return []

    def extract_locations(self, text: str) -> List[Location]:
        """
        Extracts Location Concepts.
        """
        prompt = f"""
        Identify main locations.
        Provide detailed visual description (Architecture, Mood, Colors, Lighting).
        """

        try:
            response_text = self.ai_client.generate_text(prompt + f"\nText:\n{text}", schema=list[Location])
            data = json.loads(response_text)
            return [Location(**d) for d in data]
        except Exception as e:
            logger.error(f"Error extracting locations: {e}")
            return []
