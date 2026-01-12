import json
import logging
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from illustration_gen.core.ai_client import GenAIClient
from illustration_gen.core.models import Scene, Character, Location

logger = logging.getLogger(__name__)

class StoryAnalyzer:
    def __init__(self, ai_client: GenAIClient):
        self.ai_client = ai_client

    def extract_style(self, text_segment: str, user_style_prompt: str = "") -> str:
        """
        Analyzes the text to determine a consistent visual style.
        """
        prompt = f"""
        Analyze the following text from a story and determine the most appropriate visual art style for illustrations.
        Consider the tone, genre, and setting.

        Text sample:
        "{text_segment[:2000]}..."

        User preferences (if any): {user_style_prompt}

        Output a detailed style description prompt that can be used for image generation models.
        Include details about medium (e.g., watercolor, oil, digital), lighting, color palette, and mood.
        Keep it concise but descriptive.
        """
        return self.ai_client.generate_text(prompt)

    def extract_scenes(self, text: str) -> List[Scene]:
        """
        Splits text into scenes based on Time, Location, or Action changes.
        Uses a hybrid approach: Logic splitting + AI refinement.
        """
        # 1. Split potentially large text into manageable chunks for the AI
        splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=500)
        chunks = splitter.split_text(text)

        all_scenes = []
        scene_counter = 1

        for chunk in chunks:
            # 2. Ask AI to identify scenes in this chunk
            prompt = f"""
            Analyze the following text and split it into Scenes.
            A new scene starts when there is a change in:
            1. Time (e.g., day to night, later that day)
            2. Location (e.g., moving from indoors to outdoors)
            3. Major Action (e.g., conversation ends, chase begins)

            Return a JSON list of objects. Each object must have:
            - time_of_day: str
            - location_name: str
            - characters_present: list[str]
            - action_description: str
            - visual_description: str (a prompt for an illustrator)
            - original_text_segment: str (the exact text corresponding to this scene)

            Text:
            {chunk}
            """

            # Using a simplified schema for JSON structure hint
            schema_hint = """
            [
                {
                    "time_of_day": "...",
                    "location_name": "...",
                    "characters_present": ["..."],
                    "action_description": "...",
                    "visual_description": "...",
                    "original_text_segment": "..."
                }
            ]
            """

            try:
                response_text = self.ai_client.generate_text(prompt, schema=schema_hint)
                # Clean up response if it contains markdown code blocks
                clean_json = response_text.replace("```json", "").replace("```", "").strip()
                scenes_data = json.loads(clean_json)

                for s_data in scenes_data:
                    # Create Scene object
                    scene = Scene(
                        id=scene_counter,
                        time_of_day=s_data.get("time_of_day", "Unspecified"),
                        location_name=s_data.get("location_name", "Unknown"),
                        characters_present=s_data.get("characters_present", []),
                        action_description=s_data.get("action_description", ""),
                        visual_description=s_data.get("visual_description", ""),
                        original_text_segment=s_data.get("original_text_segment", "")
                    )
                    all_scenes.append(scene)
                    scene_counter += 1

            except Exception as e:
                logger.error(f"Failed to extract scenes from chunk: {e}")
                # Fallback: Treat the whole chunk as one scene
                all_scenes.append(Scene(
                    id=scene_counter,
                    time_of_day="Unknown",
                    location_name="Unknown",
                    characters_present=[],
                    action_description="General scene",
                    visual_description="Illustration of the events described.",
                    original_text_segment=chunk
                ))
                scene_counter += 1

        return all_scenes

    def extract_characters(self, text: str) -> List[Character]:
        """
        Extracts main characters and their physical descriptions.
        """
        prompt = f"""
        Identify the active characters in the following text segment.
        For each character, provide a detailed physical description suitable for an artist (face, hair, body, clothing style).

        Return a JSON list:
        [
            {{"name": "Name", "description": "Visual description..."}}
        ]

        Text:
        {text}
        """

        try:
            response = self.ai_client.generate_text(prompt, schema="JSON List of characters")
            clean_json = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)

            return [Character(name=d["name"], description=d["description"]) for d in data]
        except Exception as e:
            logger.error(f"Error extracting characters: {e}")
            return []

    def extract_locations(self, text: str) -> List[Location]:
        """
        Extracts main locations and their visual descriptions.
        """
        prompt = f"""
        Identify the main locations in the following text segment.
        For each location, provide a detailed visual description suitable for an artist (architecture, mood, colors).

        Return a JSON list:
        [
            {{"name": "Name", "description": "Visual description..."}}
        ]

        Text:
        {text}
        """

        try:
            response = self.ai_client.generate_text(prompt, schema="JSON List of locations")
            clean_json = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)

            return [Location(name=d["name"], description=d["description"]) for d in data]
        except Exception as e:
            logger.error(f"Error extracting locations: {e}")
            return []
