from typing import List, Optional
from pydantic import BaseModel, Field

class ImageValidationResult(BaseModel):
    is_valid: bool = Field(description="True if the image PERFECTLY meets all structural rules without any violations.")
    feedback: str = Field(description="If invalid, provide EXTREMELY specific feedback on what is wrong and how the image generator must fix it in the next attempt.")

class HighlightResult(BaseModel):
    highlight_description: str = Field(description="A brief explanation of the chosen moment.")
    image_prompt: str = Field(description="A highly detailed visual description of THIS SPECIFIC MOMENT ONLY. Describe the subjects, action, lighting, and camera angle.")
    active_characters: List[str] = Field(default_factory=list, description="A list of strings containing ONLY the names of characters from the provided list that are in this moment.")

class SemanticMatchResult(BaseModel):
    match_id: Optional[int] = Field(default=None, description="The integer ID of the matched entity, or null if no match.")
    reason: str = Field(description="The reason for the match or non-match.")

class Character(BaseModel):
    id: Optional[int] = Field(default=None, description="Unique identifier for the character")
    name: str = Field(description="Name of the character")
    description: str = Field(description="Detailed physical appearance description")
    generation_prompt: Optional[str] = Field(default=None, description="The prompt used to generate the image")
    reference_image_path: Optional[str] = Field(default=None, description="Path to the generated reference image")

    full_body_path: Optional[str] = Field(default=None, description="Path to the full body reference image")
    original_name: Optional[str] = Field(default=None, description="Original name from the text")

class Location(BaseModel):
    id: Optional[int] = Field(default=None, description="Unique identifier for the location")
    name: str = Field(description="Name of the location")
    description: str = Field(description="Detailed visual description of the environment")
    generation_prompt: Optional[str] = Field(default=None, description="The prompt used to generate the image")
    reference_image_path: Optional[str] = Field(default=None, description="Path to the generated reference image")
    original_name: Optional[str] = Field(default=None, description="Original name from the text")

class Scene(BaseModel):
    id: int = Field(..., description="Sequence number of the scene (unique id)")
    start_index: int = Field(..., description="Index of the start of the scene in the original text")
    end_index: int = Field(..., description="Index of the end of the scene")
    time_of_day: str = Field(..., description="Time of day: day, night, twilight, etc.")
    location_name: str = Field(..., description="Name of the location, corresponding to the list of locations")
    characters_present: List[str] = Field(..., description="List of characters present in the scene")
    action_description: str = Field(..., description="Action description: what is happening (e.g. chase, conversation)")
    visual_description: str = Field(..., description="Detailed visual description for the illustrator")
    mood: str = Field(..., description="Mood of the scene: tense, joyful, gloomy, etc.")
    summary: str = Field(..., description="Brief summary of the scene events")
    original_text_segment: str = Field(..., description="The exact text content of the scene")
