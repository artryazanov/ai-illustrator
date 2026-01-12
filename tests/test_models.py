
import pytest
from app.core.models import Character, Location, Scene

class TestModels:
    def test_character_creation(self):
        char = Character(
            name="Hero",
            description="A brave hero",
            original_name="Hero Name"
        )
        assert char.name == "Hero"
        assert char.description == "A brave hero"
        assert char.original_name == "Hero Name"
        assert char.reference_image_path is None

    def test_location_creation(self):
        loc = Location(
            name="Dark Forest",
            description="A spooky forest",
            original_name="The Dark Forest"
        )
        assert loc.name == "Dark Forest"
        assert loc.description == "A spooky forest"
        assert loc.original_name == "The Dark Forest"
        assert loc.reference_image_path is None

    def test_scene_creation(self):
        scene = Scene(
            id=1,
            start_index=0,
            end_index=100,
            time_of_day="Night",
            location_name="Dark Forest",
            characters_present=["Hero"],
            action_description="Hero walking",
            visual_description="A dark forest with a hero walking",
            mood="Spooky",
            summary="Hero walks in forest",
            original_text_segment="Once upon a time..."
        )
        assert scene.id == 1
        assert scene.location_name == "Dark Forest"
        assert "Hero" in scene.characters_present

    def test_character_validation(self):
        with pytest.raises(ValueError):
            # Missing required fields
            Character(name="Hero") 

    def test_scene_validation(self):
        with pytest.raises(ValueError):
            Scene(id="not-an-int") # id should be int
