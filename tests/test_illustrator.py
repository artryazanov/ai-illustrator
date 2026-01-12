
import pytest
from unittest.mock import MagicMock, call, patch, mock_open
from pathlib import Path
from app.core.illustrator import StoryIllustrator
from app.core.models import Scene, Character, Location

class TestStoryIllustrator:
    @pytest.fixture
    def illustrator(self, mock_genai_client, tmp_path):
        output_dir = tmp_path / "output"
        asset_manager = MagicMock()
        asset_manager.locations = {} # Needed for .get access
        return StoryIllustrator(mock_genai_client, asset_manager, output_dir)

    def test_init_creates_dir(self, mock_genai_client, tmp_path):
        output_dir = tmp_path / "output"
        asset_manager = MagicMock()
        StoryIllustrator(mock_genai_client, asset_manager, output_dir)
        assert (output_dir / "illustrations").exists()

    def test_illustrate_scenes(self, illustrator, tmp_path):
        scene = Scene(
            id=1, start_index=0, end_index=10, time_of_day="Day", 
            location_name="Park", characters_present=["Alice"], 
            action_description="Sitting", visual_description="Sunny day", 
            mood="Calm", summary="Summary", original_text_segment="Text"
        )
        
        # Mock asset manager data
        char_data = Character(name="Alice", description="Desc", portrait_path="p.jpg", full_body_path="f.jpg")
        illustrator.asset_manager.get_character_data.return_value = char_data
        illustrator.asset_manager.get_location_ref.return_value = "loc_ref.jpg"

        # Mock AI slug generation
        illustrator.ai_client.generate_filename_slug.return_value = "sunny_day"
        
        # Test execute
        with patch("builtins.open", mock_open()) as mocked_file:
             illustrator.illustrate_scenes([scene], "style")

        # Verify Scene Folder Creation - UPDATED: No folder, direct file
        # We can't check file existence with mock_open easily if the code didn't try to open it to WRITE 
        # (ai_client.generate_image writes content, but that is mocked too).
        # We check the calls.

        # Verify JSON writing (metadata + global data.json)
        # We expect open calls for data.json
        assert mocked_file.call_count == 1
        
        # Verify Image Generation
        illustrator.ai_client.generate_image.assert_called_once()
        args, kwargs = illustrator.ai_client.generate_image.call_args
        
        # Check output path matches new structure
        expected_path = str(illustrator.output_dir / "1_sunny_day.jpeg")
        assert kwargs['output_path'] == expected_path

        assert "Park" in kwargs['prompt'] # Check prompt construction
        assert len(kwargs['reference_images']) == 2
        # Check Character Ref
        assert kwargs['reference_images'][0]['path'] == "f.jpg"
        assert kwargs['reference_images'][0]['purpose'] == "Character Appearance Reference for Alice"
        # Check Location Ref
        assert kwargs['reference_images'][1]['path'] == "loc_ref.jpg"
        assert kwargs['reference_images'][1]['purpose'] == "Location Environment Reference"

    def test_select_character_ref_portrait(self, illustrator):
        scene = Scene(
            id=1, start_index=0, end_index=0, time_of_day="", location_name="", 
            characters_present=[], action_description="", visual_description="close-up on face", 
            mood="", summary="", original_text_segment=""
        )
        char = Character(name="C", description="", portrait_path="p.jpg", full_body_path="f.jpg")
        illustrator.asset_manager.get_character_data.return_value = char
        
        ref = illustrator._select_character_ref("C", scene)
        assert ref == "f.jpg"

    def test_select_character_ref_fullbody(self, illustrator):
        scene = Scene(
            id=1, start_index=0, end_index=0, time_of_day="", location_name="", 
            characters_present=[], action_description="", visual_description="Running away", 
            mood="", summary="", original_text_segment=""
        )
        char = Character(name="C", description="", portrait_path="p.jpg", full_body_path="f.jpg")
        illustrator.asset_manager.get_character_data.return_value = char
        
        ref = illustrator._select_character_ref("C", scene)
        assert ref == "f.jpg"
