
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from app.core.asset_manager import AssetManager

@pytest.fixture
def mock_client():
    from app.core.ai_client import GenAIClient
    return MagicMock(spec=GenAIClient)

@pytest.fixture
def asset_manager(mock_client, tmp_path):
    output_dir = tmp_path / "output"
    return AssetManager(mock_client, output_dir)

def test_prepare_style_templates_uses_bg_landscape_ref(asset_manager):
    # Mock exists to return False for bg_f so it tries to generate
    # We need strictly controlled side effects for exists()
    # 1. bg_f exists? -> False (so we generate it)
    # 2. etc.
    
    # Simpler: just patch exists to return False globally for this test context or use side_effect
    with patch.object(Path, 'exists', return_value=False):
        asset_manager.prepare_style_templates("anime")
        
        # Verify generate_image calls
        # We expect calls for bg_f and ref_f
        
        # Filter calls for bg_f
        # We look for the call where output_path ends with bg_fullbody.jpg
        calls = asset_manager.ai_client.generate_image.call_args_list
        
        bg_f_call = None
        for call in calls:
            if "bg_fullbody.jpg" in str(call.kwargs.get('output_path', '')):
                bg_f_call = call
                break
        
        assert bg_f_call is not None
        
        # Check reference paths
        refs = bg_f_call.kwargs.get('reference_images', [])
        assert len(refs) == 1
        assert "bg_location_16_9.jpg" in refs[0]['path']
        assert refs[0]['purpose'] == "Style Reference"
