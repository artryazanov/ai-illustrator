import json
import logging
from typing import List

from app.core.ai_client import GenAIClient
from app.core.models import Scene, Character, Location

logger = logging.getLogger(__name__)

class StoryAnalyzer:
    def __init__(self, ai_client: GenAIClient):
        self.ai_client = ai_client

    def simple_text_splitter(self, text: str, chunk_size: int = 50000, overlap: int = 1000) -> List[str]:
        """
        Splits text into large chunks (e.g., chapters) using semantic boundaries like paragraphs.
        """
        if len(text) <= chunk_size:
            return [text]
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = min(start + chunk_size, text_len)
            
            if end < text_len:
                search_start = max(start, end - overlap)
                break_pos = text.rfind('\n\n', search_start, end)
                
                if break_pos == -1:
                    break_pos = text.rfind('\n', search_start, end)
                if break_pos == -1:
                    break_pos = text.rfind('. ', search_start, end)
                if break_pos == -1:
                    break_pos = text.rfind(' ', search_start, end)
                
                if break_pos != -1:
                    if text[break_pos:break_pos+2] in ('\n\n', '. '):
                        end = break_pos + 2
                    else:
                        end = break_pos + 1
            
            chunks.append(text[start:end])
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
        chunks = self.simple_text_splitter(text, chunk_size=50000, overlap=1000)

        all_scenes = []
        scene_counter = 1
        running_context_summary = "Start of the story."

        for chunk_idx, chunk in enumerate(chunks):
            logger.info(f"Analyzing chunk {chunk_idx + 1}/{len(chunks)} for scenes...")
            
            prompt = f"""
            Analyze the following text and split it into logical Scenes.
            A new scene starts when there is a change in:
            1. Time (e.g., day to night, later that day)
            2. Location (e.g., moving from indoors to outdoors)
            3. Major Action (e.g., conversation ends, chase begins)

            [PREVIOUS CONTEXT SUMMARY (For Reference Only)]
            {running_context_summary}

            Return a List of Scene objects based ONLY on the new chunk Text below.
            """

            try:
                response_data = self.ai_client.generate_text(prompt + f"\nText:\n{chunk}", schema=list[Scene])
                
                data_list = []
                if isinstance(response_data, list):
                    # Natively parsed by SDK via response.parsed
                    data_list = [item.model_dump() if hasattr(item, 'model_dump') else item for item in response_data]
                else:
                    clean_text = response_data.replace("```json", "").replace("```", "").strip()
                    data_list = json.loads(clean_text)
                
                if isinstance(data_list, list):
                    sorted_data = sorted(data_list, key=lambda x: isinstance(x, dict) and x.get('start_index', 0) or getattr(x, 'start_index', 0))
                    for s_data in sorted_data:
                        if isinstance(s_data, dict):
                            scene = Scene(**s_data)
                        else:
                            scene = s_data
                        
                        scene.id = scene_counter 
                        scene_counter += 1
                        all_scenes.append(scene)
                else:
                    logger.warning("Model returned non-list data for scenes.")
                    
            except Exception as e:
                logger.error(f"Failed to extract scenes from chunk: {e}")
            
            if chunk_idx < len(chunks) - 1:
                summary_prompt = f"Summarize the events and characters in this text chunk to context for the next split. Keep it under 150 words.\n\nText:\n{chunk[-5000:]}"
                try:
                    running_context_summary = self.ai_client.generate_text(summary_prompt)
                except Exception as e:
                    logger.warning(f"Failed to generate chunk context summary: {e}")

        return all_scenes

    def extract_characters(self, text: str) -> List[Character]:
        """
        Extracts Character Sheets (Visual Descriptions).
        """
        prompt = f"""
        Analyze the text and identify key characters.
        Create a **HIGHLY DETAILED** Visual Portrait for each.
        
        You must provide a comprehensive physical description including:
        - **Face**: Eye color/shape, nose, mouth, jawline, skin texture/tone, facial hair, makeup.
        - **Hair**: Exact color, style, length, texture.
        - **Physique**: Body type, height, posture, build.
        - **Outfit**: Detailed clothing breakdown (top, bottom, shoes, accessories), colors, materials, style (e.g., worn leather, silk robes).
        - **Distinctive Features**: Scars, tattoos, jewelry, glasses, weapons, props.
        
        The description must be vivid and specific enough for an artist to paint an exact replica without guessing. 
        Avoid abstract personality traits (e.g., "kind", "brave") unless they manifest visually (e.g., "kind eyes", "confident stance").
        Focus ONLY on visual traits.
        """

        try:
            response_data = self.ai_client.generate_text(prompt + f"\nText:\n{text}", schema=list[Character])
            if isinstance(response_data, list):
                return [ch if isinstance(ch, Character) else Character(**(ch.model_dump() if hasattr(ch, 'model_dump') else ch)) for ch in response_data]
            
            clean_text = response_data.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
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
            response_data = self.ai_client.generate_text(prompt + f"\nText:\n{text}", schema=list[Location])
            if isinstance(response_data, list):
                return [loc if isinstance(loc, Location) else Location(**(loc.model_dump() if hasattr(loc, 'model_dump') else loc)) for loc in response_data]
            
            clean_text = response_data.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            return [Location(**d) for d in data]
        except Exception as e:
            logger.error(f"Error extracting locations: {e}")
            return []
