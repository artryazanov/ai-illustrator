
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

def test_prepare_style_templates_isolated_character(asset_manager):
    with patch.object(Path, 'exists', return_value=False):
        asset_manager.prepare_style_templates("anime")
        
        calls = asset_manager.ai_client.generate_image.call_args_list
        ref_f_call = None
        for call in calls:
            if "style_reference_fullbody.jpg" in str(call.kwargs.get('output_path', '')):
                ref_f_call = call
                break
        
        assert ref_f_call is not None
        assert "PURE WHITE background" in ref_f_call.args[0]
        assert len(ref_f_call.kwargs.get('reference_images', [])) == 0

def test_prepare_style_templates_qa_retry(asset_manager):
    from app.core.models import ImageValidationResult
    fail_res = ImageValidationResult(is_valid=False, feedback="Bad body")
    succ_res = ImageValidationResult(is_valid=True, feedback="")
    asset_manager.ai_client.validate_image.side_effect = [fail_res, succ_res]
    
    with patch.object(Path, 'exists', return_value=False):
        asset_manager.prepare_style_templates("anime")
        
        assert asset_manager.ai_client.validate_image.call_count == 2
        calls = asset_manager.ai_client.generate_image.call_args_list
        # Second call should have feedback in prompt
        assert "[CRITICAL CORRECTION REQUIRED]" in calls[1].args[0]

def test_prepare_style_templates_exception(asset_manager):
    asset_manager.ai_client.generate_image.side_effect = Exception("API error")
    with patch.object(Path, 'exists', return_value=False):
        asset_manager.prepare_style_templates("anime")
        # Should not crash, just hit max retries
        assert asset_manager.ai_client.generate_image.call_count == 3
