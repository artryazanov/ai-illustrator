
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from app.core.asset_manager import AssetManager
from app.core.models import Location

@pytest.fixture
def mock_client():
    from app.core.ai_client import GenAIClient
    return MagicMock(spec=GenAIClient)

@pytest.fixture
def asset_manager(mock_client, tmp_path):
    output_dir = tmp_path / "output"
    return AssetManager(mock_client, output_dir)

def test_prepare_location_templates_only_bg(asset_manager):
    # Mock exists to return False so it tries to generate
    with patch.object(Path, 'exists', return_value=False):
        asset_manager.prepare_location_templates("style")
        
        # Should call generate_image exactly once (for bg_landscape)
        # because we removed ref_landscape generation
        assert asset_manager.ai_client.generate_image.call_count == 1
        
        # Verify the call was for bg_landscape
        call_args = asset_manager.ai_client.generate_image.call_args
        assert "bg_location_16_9.jpg" in str(call_args[1]['output_path'])

def test_generate_location_assets_uses_only_bg_ref(asset_manager):
    asset_manager.ai_client.translate_to_english.return_value = "Forest"
    loc = Location(name="Forest", description="Trees", original_name="Forest")
    
    # Mock exists so we don't try to generate templates
    with patch.object(Path, 'exists', return_value=True):
        asset_manager.generate_location_assets([loc], "style")
        
        # Check call arguments for location generation
        args, kwargs = asset_manager.ai_client.generate_image.call_args
        
        # reference_images should contain ONLY bg_landscape
        refs = kwargs['reference_images']
        assert len(refs) == 1
        assert "bg_location_16_9.jpg" in refs[0]['path']
        assert refs[0]['purpose'] == "Environment Style Template"
