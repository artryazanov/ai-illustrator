from typing import List, Optional
from pydantic import BaseModel, Field

class Character(BaseModel):
    name: str = Field(description="Name of the character")
    description: str = Field(description="Detailed physical appearance description")
    reference_image_path: Optional[str] = Field(default=None, description="Path to the generated reference image")

class Location(BaseModel):
    name: str = Field(description="Name of the location")
    description: str = Field(description="Detailed visual description of the environment")
    reference_image_path: Optional[str] = Field(default=None, description="Path to the generated reference image")

class Scene(BaseModel):
    id: int = Field(description="Sequence number of the scene")
    time_of_day: str = Field(description="Time of day (e.g., Morning, Night, Noon)")
    location_name: str = Field(description="Name of the location where the scene takes place")
    characters_present: List[str] = Field(description="List of character names present in the scene")
    action_description: str = Field(description="What is happening in the scene")
    visual_description: str = Field(description="A detailed visual prompt description for this specific scene")
    original_text_segment: str = Field(description="The original text segment covering this scene")
