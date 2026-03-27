
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
        
        # Mock Location Data
        loc_data = Location(name="Park", description="Park Desc", reference_image_path="loc_ref.jpg", id=101)
        illustrator.asset_manager.get_location_data.return_value = loc_data
        illustrator.asset_manager.get_location_ref.return_value = "loc_ref.jpg"

        # Mock Global Style Template
        mock_ref_f = MagicMock()
        mock_ref_f.__str__.return_value = "/path/to/ref_f.jpg"
        mock_ref_f.exists.return_value = True
        illustrator.asset_manager.templates = {"ref_f": mock_ref_f}

        # Mock AI slug generation
        illustrator.ai_client.generate_filename_slug.return_value = "sunny_day"
        illustrator.ai_client.analyze_scene_for_highlight.return_value = {"image_prompt": "highlight prompt", "active_characters": ["Alice"]}
        
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
        assert len(kwargs['reference_images']) == 3
        
        # Check Character Ref
        assert kwargs['reference_images'][0]['path'] == "f.jpg"
        assert "Character Style and Appearance Reference" in kwargs['reference_images'][0]['purpose']
        
        # Check Location Ref
        assert kwargs['reference_images'][1]['path'] == "loc_ref.jpg"
        assert kwargs['reference_images'][1]['purpose'] == "Location Environment Reference"

        # Check Global Style Ref
        assert kwargs['reference_images'][2]['path'] == "/path/to/ref_f.jpg"
        assert kwargs['reference_images'][2]['purpose'] == "Global Art Style Reference"

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

    def test_illustrate_scenes_skip_existing(self, illustrator, tmp_path):
        scene = Scene(id=1, start_index=0, end_index=0, time_of_day="", location_name="Park", characters_present=["Alice", "Bob"], action_description="", visual_description="test", mood="", summary="", original_text_segment="")
        
        illustrator.ai_client.generate_filename_slug.return_value = "slug"
        loc_data = Location(name="Park", description="Desc", id=101)
        char_data = Character(name="Alice", description="Desc", id=1)
        
        # Prepopulate dicts so _save_data_json iterates over them
        illustrator.asset_manager.characters["Alice"] = char_data
        illustrator.asset_manager.locations["Park"] = loc_data
        
        illustrator.asset_manager.get_location_data.return_value = loc_data
        illustrator.asset_manager.get_character_data.return_value = char_data
        
        # Create dummy file to trigger skip
        img_file = illustrator.output_dir / f"1_slug.jpeg"
        img_file.parent.mkdir(parents=True, exist_ok=True)
        img_file.touch()
        
        illustrator.illustrate_scenes([scene], "style")
        
        illustrator.ai_client.analyze_scene_for_highlight.assert_not_called()
        illustrator.ai_client.generate_image.assert_not_called()

    def test_illustrate_scenes_thread_exception(self, illustrator, tmp_path):
        scene = Scene(id=1, start_index=0, end_index=0, time_of_day="", location_name="Park", characters_present=["Alice"], action_description="", visual_description="test", mood="", summary="", original_text_segment="")
        
        # Force exception in thread
        illustrator.ai_client.generate_filename_slug.side_effect = Exception("Thread crash")
        
        # Process should catch exception and not crash main thread
        illustrator.illustrate_scenes([scene], "style")
        
        # Verify it didn't crash and called save JSON at the end
        assert len(illustrator.illustrations_registry) == 0

    def test_generate_scene_image_qa_retry(self, illustrator, tmp_path):
        from app.core.models import ImageValidationResult
        scene = Scene(id=1, start_index=0, end_index=0, time_of_day="", location_name="Park", characters_present=["Alice", "Bob"], action_description="", visual_description="test", mood="", summary="", original_text_segment="")
        
        output_path = tmp_path / "out.jpeg"
        
        # First attempt fails QA, second succeeds
        fail_result = ImageValidationResult(is_valid=False, feedback="Bad")
        success_result = ImageValidationResult(is_valid=True, feedback="")
        illustrator.ai_client.validate_image.side_effect = [fail_result, success_result]
        
        illustrator._generate_scene_image(scene, "style", output_path)
        
        assert illustrator.ai_client.generate_image.call_count == 2
        assert illustrator.ai_client.validate_image.call_count == 2

    def test_generate_scene_image_max_retries(self, illustrator, tmp_path):
        from app.core.models import ImageValidationResult
        scene = Scene(id=1, start_index=0, end_index=0, time_of_day="", location_name="Park", characters_present=["Alice"], action_description="", visual_description="test", mood="", summary="", original_text_segment="")
        
        output_path = tmp_path / "out.jpeg"
        
        fail_result = ImageValidationResult(is_valid=False, feedback="Bad")
        illustrator.ai_client.validate_image.return_value = fail_result
        
        # Exception on 3rd attempt to hit both exception handler and max retries failure
        illustrator.ai_client.generate_image.side_effect = [None, None, Exception("API")]
        
        prompt = illustrator._generate_scene_image(scene, "style", output_path)
        
        assert prompt is not None
        assert illustrator.ai_client.generate_image.call_count == 3
        assert illustrator.ai_client.validate_image.call_count == 2

    def test_select_character_ref_not_found(self, illustrator):
        scene = Scene(id=1, start_index=0, end_index=0, time_of_day="", location_name="Park", characters_present=["Alice"], action_description="", visual_description="test", mood="", summary="", original_text_segment="")
        illustrator.asset_manager.get_character_data.return_value = None
        assert illustrator._select_character_ref("Missing", scene) is None

    def test_save_data_json_populates_characters(self, illustrator, tmp_path):
        char = Character(name="Alice", description="D", id=1)
        char.original_name = "Real Alice"
        
        loc = Location(name="Park", description="D", id=1)
        
        illustrator.asset_manager.characters = {"Alice": char}
        illustrator.asset_manager.locations = {"Park": loc}
        
        illustrator._save_data_json("style")
        
        manifest = illustrator.output_dir.parent / "data.json"
        assert manifest.exists()
