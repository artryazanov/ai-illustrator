import json
import pytest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner
import main
from app.core.models import Scene, Character, Location

def test_main_sync_logic(tmp_path):
    """
    Tests that main.py correctly synchronizes scene entities with actual extracted names.
    """
    runner = CliRunner()
    
    # Create dummy text file
    text_file = tmp_path / "story.txt"
    text_file.write_text("Dummy story text", encoding='utf-8')
    
    output_dir = tmp_path / "output"

    # We need to mock components used in main.py to isolate the sync logic
    with patch('main.Config.validate') as mock_validate, \
         patch('main.GenAIClient') as mock_genai_client, \
         patch('main.StoryAnalyzer') as mock_story_analyzer, \
         patch('main.AssetManager') as mock_asset_manager, \
         patch('main.StoryIllustrator') as mock_illustrator:
             
        # Create a mock scene with initial Russian/original names
        initial_scene = Scene(
            id=1,
            start_index=0,
            end_index=10,
            time_of_day="Day",
            location_name="Изба", # Initial name
            characters_present=["Старик", "Старуха"], # Initial names
            action_description="Action",
            visual_description="Vis",
            mood="Mood",
            summary="Sum",
            original_text_segment="Segment"
        )
        
        # Setup the analyzer mock to return our scene, characters and locations
        mock_analyzer_instance = MagicMock()
        mock_analyzer_instance.extract_style.return_value = "Style"
        mock_analyzer_instance.extract_scenes.return_value = [initial_scene]
        
        # The analyzer should return English translation Character/Location models
        extracted_char_1 = Character(name="The Old Man", description="x", original_name="Старик")
        extracted_char_2 = Character(name="The Old Woman", description="y", original_name="Старуха")
        mock_analyzer_instance.extract_characters.return_value = [extracted_char_1, extracted_char_2]
        
        extracted_loc = Location(name="Old Couple's Hut", description="z", original_name="Изба")
        mock_analyzer_instance.extract_locations.return_value = [extracted_loc]
        
        mock_story_analyzer.return_value = mock_analyzer_instance
        
        # Run main to trigger the loop
        result = runner.invoke(main.main, ['--text-file', str(text_file), '--output-dir', str(output_dir)])
        
        assert result.exit_code == 0
        
        # Verify that the scene attributes were synchronized!
        assert initial_scene.characters_present == ["The Old Man", "The Old Woman"]
        assert initial_scene.location_name == "Old Couple's Hut"
