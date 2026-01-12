from unittest.mock import MagicMock
import pytest
from pathlib import Path
import json
from app.core.asset_manager import AssetManager
from app.core.illustrator import StoryIllustrator
from app.core.models import Character, Location, Scene

def test_prompt_saving(tmp_path):
    # Setup
    mock_ai_client = MagicMock()
    mock_ai_client.translate_to_english.return_value = "Test_Item"
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    asset_manager = AssetManager(mock_ai_client, output_dir)
    illustrator = StoryIllustrator(mock_ai_client, asset_manager, output_dir)
    
    # 1. Test Character Prompt Saving
    char = Character(name="Test Char", description="A test character")
    # Simulate generation
    asset_manager.templates["ref_f"] = MagicMock() # Mock template existence
    asset_manager.templates["ref_f"].exists.return_value = True
    
    # Mock generate_image key side effect to not fail
    pass
    
    asset_manager.generate_character_assets([char], "Anime Style")
    
    # Check if prompt was saved in object
    assert char.generation_prompt is not None, "Character prompt not saved in object"
    assert "Test Char" in char.generation_prompt
    
    # 2. Test Location Prompt Saving
    loc = Location(name="Test Loc", description="A test location")
    asset_manager.loc_templates["bg_landscape"] = MagicMock()
    asset_manager.loc_templates["bg_landscape"].exists.return_value = True
    
    asset_manager.generate_location_assets([loc], "Anime Style")
    
    assert loc.generation_prompt is not None, "Location prompt not saved in object"
    assert "Test Loc" in loc.generation_prompt
    
    # 3. Test Illustration Prompt Saving
    scene = Scene(
        id=1, start_index=0, end_index=10, time_of_day="Day",
        location_name="Test Loc", characters_present=["Test Char"],
        action_description="Standing", visual_description="A scene",
        mood="Happy", summary="A summary", original_text_segment="Text"
    )
    
    # We need to make sure the mock client returns something if needed, 
    # but generate_image returns None. 
    # In illustrator code:
    # prompt = self._generate_scene_image(...)
    
    # wait, _generate_scene_image generates the prompt string internally and returns it.
    # It calls ai_client.generate_image but that returns None (or whatever).
    # The return value of _generate_scene_image is the *prompt string* constructed inside it.
    
    illustrator.illustrate_scenes([scene], "Anime Stylen")
    
    # 4. Verify data.json
    data_path = output_dir / "data.json"
    assert data_path.exists()
    
    with open(data_path, "r") as f:
        data = json.load(f)
        
    # Check Characters
    saved_char = data["characters"][0]
    assert saved_char["name"] == "Test Char"
    assert "generation_prompt" in saved_char
    assert saved_char["generation_prompt"] == char.generation_prompt
    
    # Check Locations
    saved_loc = data["locations"][0]
    assert saved_loc["name"] == "Test Loc"
    assert "generation_prompt" in saved_loc
    assert saved_loc["generation_prompt"] == loc.generation_prompt
    
    # Check Illustrations
    saved_scene = data["illustrations"][0]
    assert saved_scene["scene_id"] == 1
    assert "generation_prompt" in saved_scene
    assert saved_scene["generation_prompt"] is not None
    assert "A scene" in saved_scene["generation_prompt"]

if __name__ == "__main__":
    pytest.main([__file__])
