
import pytest
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path
from illustration_gen.core.asset_manager import AssetManager
from illustration_gen.core.models import Character, Location

@pytest.fixture
def mock_wrapper_client():
    from illustration_gen.core.ai_client import GenAIClient
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
            # bg_p, bg_f, ref_p, ref_f = 4 calls
            assert asset_manager.ai_client.generate_image.call_count >= 4

    def test_load_catalog(self, asset_manager):
        catalog_content = '[{"name": "Hero", "description": "Desc", "original_name": "Hero"}]'
        
        # We need to ensure the catalog path "exists"
        with patch.object(Path, 'exists', return_value=True):
            # Mock open to read content
            with patch("builtins.open", mock_open(read_data=catalog_content)):
                # clear and reload
                asset_manager.characters = {}
                asset_manager._load_catalog()
                
                assert "Hero" in asset_manager.characters
                assert asset_manager.characters["Hero"].description == "Desc"

    def test_generate_character_assets_new(self, asset_manager):
        asset_manager.ai_client.translate_to_english.return_value = "Hero"
        char = Character(name="Герой", description="A hero", original_name="Герой")
        
        # Mock generate_image to succeed
        asset_manager.ai_client.generate_image.return_value = None
        
        with patch("builtins.open", mock_open()): # Mock file writing for description
             asset_manager.generate_character_assets([char], "anime style")
        
        # Should translate name
        asset_manager.ai_client.translate_to_english.assert_called_with("Герой")
        # Should call generate_image twice (portrait + full body)
        assert asset_manager.ai_client.generate_image.call_count == 2
        # Should be added to catalog
        assert "Герой" in asset_manager.characters

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
        assert char.portrait_path == "path/to/p.jpg"

    def test_generate_location_assets(self, asset_manager):
            asset_manager.ai_client.translate_to_english.return_value = "Forest"
            loc = Location(name="Les", description="Forest", original_name="Les")
            
            asset_manager.ai_client.generate_image.return_value = None
            
            asset_manager.generate_location_assets([loc], "style")
            
            asset_manager.ai_client.translate_to_english.assert_called_with("Les")
            # Logic: verify it calls generate_image for the location card ONCE
            assert asset_manager.ai_client.generate_image.call_count == 1
            assert "Les" in asset_manager.locations
