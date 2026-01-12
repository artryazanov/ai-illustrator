
import pytest
import json
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
from app.core.asset_manager import AssetManager
from app.core.models import Character, Location

@pytest.fixture
def mock_wrapper_client():
    from app.core.ai_client import GenAIClient
    client = MagicMock(spec=GenAIClient)
    return client

@pytest.fixture
def asset_manager(mock_wrapper_client, tmp_path):
    output_dir = tmp_path / "output"
    return AssetManager(mock_wrapper_client, output_dir)

class TestAssetManager:
    def test_init_creates_directories(self, mock_wrapper_client, tmp_path):
        output_dir = tmp_path / "output"
        AssetManager(mock_wrapper_client, output_dir)
        
        # Only style_templates is created in __init__
        assert (output_dir / "style_templates").exists()

    def test_prepare_style_templates(self, asset_manager):
        # Mock exists to return False so it tries to generate
        with patch.object(Path, 'exists', return_value=False):
            asset_manager.prepare_style_templates("anime")
            
            # Check if generate_image was called for templates
            # bg_f, ref_f = 2 calls (portrait ones removed)
            assert asset_manager.ai_client.generate_image.call_count >= 2

    def test_load_data(self, asset_manager):
        # Mock data.json content
        data_content = json.dumps({
            "characters": [{"name": "Hero", "description": "Desc", "original_name": "Hero"}],
            "locations": [{"name": "Town", "description": "Place", "original_name": "Town"}]
        })
        
        # We need to ensure the data path "exists"
        with patch.object(Path, 'exists', return_value=True):
            # Mock open to read content
            with patch("builtins.open", mock_open(read_data=data_content)):
                # clear and reload
                asset_manager.characters = {}
                asset_manager.locations = {}
                asset_manager._load_data()
                
                assert "Hero" in asset_manager.characters
                assert asset_manager.characters["Hero"].description == "Desc"
                assert "Town" in asset_manager.locations
                assert "Town" in asset_manager.locations

    def test_migrate_legacy_data(self, asset_manager):
        # Mock no data.json
        with patch.object(Path, 'exists', side_effect=lambda: False): # data.json doesn't exist
            # Mock legacy files exist
            with patch("pathlib.Path.exists", side_effect=lambda: True):
                # Mock read content
               legacy_char = '[{"name": "OldHero", "description": "D", "original_name": "OldHero"}]'
               legacy_loc = '[{"name": "OldTown", "description": "L", "original_name": "OldTown"}]'
               
               with patch("builtins.open", mock_open(read_data=legacy_char)) as m:
                   # Managing multiple opens is tricky with mock_open, we can use side_effect for open 
                   # but simplified verify: calls _migrate_legacy_data
                   asset_manager._migrate_legacy_data()
                   
                   # Since we can't easily mock separate file contents with simple mock_open in one go without complex side_effects,
                   # we rely on the logic that if it runs without error and attempts to parse, it works.
                   # Ideally we'd use a real tmp_path for this test.
                   pass

    def test_migrate_logic_real_files(self, mock_wrapper_client, tmp_path):
        # Better test with real files
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        (output_dir / "characters").mkdir()
        (output_dir / "locations").mkdir()
        
        # Write legacy files
        char_file = output_dir / "characters" / "characters.json"
        loc_file = output_dir / "locations" / "locations.json"
        
        with open(char_file, "w") as f:
            f.write('[{"name": "OldHero", "description": "D", "original_name": "OldHero"}]')
            
        with open(loc_file, "w") as f:
             f.write('[{"name": "OldTown", "description": "L", "original_name": "OldTown"}]')
             
        mgr = AssetManager(mock_wrapper_client, output_dir)
        # It should try to load data.json (not exist) -> migrate -> properties populated
        
        assert "OldHero" in mgr.characters
        assert "OldTown" in mgr.locations
        assert (output_dir.parent / "data.json").exists()
        

    def test_generate_character_assets_existing(self, asset_manager):
        char = Character(name="Hero", description="Desc", original_name="Hero")
        existing_char = Character(
            name="Hero", description="Desc", original_name="Hero",
            portrait_path="path/to/p.jpg", full_body_path="path/to/f.jpg"
        )
        asset_manager.characters["Hero"] = existing_char
        
        asset_manager.generate_character_assets([char], "style")
        
        # Should NOT call generate image
        asset_manager.ai_client.generate_image.assert_not_called()
        # Should update the submitted char object with paths
        # assert char.portrait_path == "path/to/p.jpg" # Removed portrait path update logic
        assert char.full_body_path == "path/to/f.jpg"

    def test_generate_location_assets(self, asset_manager):
            asset_manager.ai_client.translate_to_english.return_value = "Forest"
            loc = Location(name="Les", description="Forest", original_name="Les")
            
            asset_manager.ai_client.generate_image.return_value = None
            
            asset_manager.generate_location_assets([loc], "style")
            
            asset_manager.ai_client.translate_to_english.assert_called_with("Les")
            # Logic: verify it calls generate_image for the location card ONCE
            assert asset_manager.ai_client.generate_image.call_count == 1
            assert "Les" in asset_manager.locations
    def test_load_data_error(self, asset_manager):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = Exception("Read Error")
            # Should catch exception and log error, not crash
            asset_manager._load_data()
            
    def test_save_data_error(self, asset_manager):
        with patch("builtins.open", mock_open()) as m:
            m.side_effect = Exception("Write Error")
            # Should catch exception and log error, not crash
            asset_manager._save_data()

    def test_migrate_legacy_data_error(self, asset_manager):
        with patch.object(Path, 'exists', side_effect=lambda: False): # data.json missing
             with patch("pathlib.Path.exists", side_effect=lambda: True): # legacy files exist
                 with patch("builtins.open", side_effect=Exception("Migrate Error")):
                     asset_manager._migrate_legacy_data()

    def test_generate_character_assets_new(self, asset_manager, tmp_path):
        asset_manager.ai_client.translate_to_english.return_value = "New Guy"
        char = Character(name="New Guy", description="Desc")
        
        # Mock generate_image success
        asset_manager.ai_client.generate_image.return_value = "path/to/img.jpg"
        
        asset_manager.generate_character_assets([char], "style")
        
        assert char.id is not None
        assert "New Guy" in asset_manager.characters
        asset_manager.ai_client.generate_image.assert_called_once()

    def test_generate_character_assets_failure(self, asset_manager):
        asset_manager.ai_client.translate_to_english.return_value = "Fail Guy"
        char = Character(name="Fail Guy", description="Desc")
        
        asset_manager.ai_client.generate_image.side_effect = Exception("Gen Fail")
        
        asset_manager.generate_character_assets([char], "style")
        
        # Should not crash, just log error
        assert char.full_body_path is None

    def test_get_character_data_partial(self, asset_manager):
        asset_manager.characters = {"Alice In Wonderland": Character(name="Alice In Wonderland", description="")}
        
        char = asset_manager.get_character_data("Alice")
        assert char is not None
        assert char.name == "Alice In Wonderland"
        
        char = asset_manager.get_character_data("Wonderland")
        assert char is not None
        
        char = asset_manager.get_character_data("Bob")
        assert char is None

    def test_generate_location_assets_skip_existing(self, asset_manager):
        loc = Location(name="Existing", description="D", original_name="Existing")
        asset_manager.locations["Existing"] = loc
        
        asset_manager.generate_location_assets([loc], "style")
        asset_manager.ai_client.generate_image.assert_not_called()

    def test_generate_location_assets_failure(self, asset_manager):
        asset_manager.ai_client.translate_to_english.return_value = "Fail Loc"
        loc = Location(name="Fail Loc", description="D")
        
        asset_manager.ai_client.generate_image.side_effect = Exception("Loc Fail")
        
        asset_manager.generate_location_assets([loc], "style")
        # Should catch exception
        assert loc.reference_image_path is None
