from typing import List, Optional
from pydantic import BaseModel, Field

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
