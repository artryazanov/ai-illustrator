
import pytest
from unittest.mock import MagicMock, patch
from app.core.ai_client import GenAIClient
from PIL import Image

@pytest.fixture
def ai_client(mock_genai_client):
    return GenAIClient()

class TestGenAIClient:
    def test_generate_text(self, ai_client, mock_genai_client):
        # Setup mock response on the instance returned by the constructor
        mock_instance = mock_genai_client.return_value
        mock_response = MagicMock()
        mock_response.text = "Generated text"
        mock_instance.models.generate_content.return_value = mock_response

        text = ai_client.generate_text("prompt")
        
        assert text == "Generated text"
        mock_instance.models.generate_content.assert_called_once()
        args, kwargs = mock_instance.models.generate_content.call_args
        assert kwargs['model'] == ai_client.text_model_name

    def test_translate_to_english(self, ai_client):
        # Mock generate_text since translate calls it
        # This mocks the method on the ai_client instance we are testing
        with patch.object(ai_client, 'generate_text', return_value="Translation"):
            result = ai_client.translate_to_english("Original")
            assert result == "Translation"
            ai_client.generate_text.assert_called()

    def test_generate_image(self, ai_client, mock_genai_client, tmp_path):
        # Prepare mock response with image part
        mock_instance = mock_genai_client.return_value
        mock_response = MagicMock()
        mock_part = MagicMock()
        mock_part.image = MagicMock()
        mock_part.image.image_bytes = b"fake_image_bytes"
        mock_response.parts = [mock_part]
        
        mock_instance.models.generate_content.return_value = mock_response
        
        output_path = tmp_path / "test_image.jpg"
        
        result = ai_client.generate_image("prompt", output_path=str(output_path))
        
        assert result == str(output_path)
        assert output_path.exists()
        assert output_path.read_bytes() == b"fake_image_bytes"
        
        # Verify call arguments
        args, kwargs = mock_instance.models.generate_content.call_args
        assert "response_modalities" in kwargs['config'].model_dump()
        assert kwargs['model'] == ai_client.image_model_name

    def test_generate_text_with_schema(self, ai_client, mock_genai_client):
        mock_instance = mock_genai_client.return_value
        mock_response = MagicMock()
        mock_response.text = '{"key": "value"}'
        mock_instance.models.generate_content.return_value = mock_response

        schema = MagicMock()
        text = ai_client.generate_text("prompt", schema=schema)
        
        assert text == '{"key": "value"}'
        args, kwargs = mock_instance.models.generate_content.call_args
        assert kwargs['config']['response_mime_type'] == 'application/json'
        assert kwargs['config']['response_schema'] == schema

    def test_generate_text_exception(self, ai_client, mock_genai_client):
        mock_instance = mock_genai_client.return_value
        mock_instance.models.generate_content.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="API Error"):
            ai_client.generate_text("prompt")

    def test_translate_to_english_exception(self, ai_client):
        with patch.object(ai_client, 'generate_text', side_effect=Exception("Trans Error")):
            result = ai_client.translate_to_english("Original")
            assert result == "Original" 

    def test_generate_filename_slug(self, ai_client):
        with patch.object(ai_client, 'generate_text', return_value="my_slug"):
            slug = ai_client.generate_filename_slug("desc")
            assert slug == "my_slug"
            
    def test_generate_filename_slug_exception(self, ai_client):
        with patch.object(ai_client, 'generate_text', side_effect=Exception("Slug Error")):
            slug = ai_client.generate_filename_slug("desc")
            assert slug == "scene"

    def test_analyze_scene_for_highlight(self, ai_client):
        mock_json = '{"highlight_description": "H", "image_prompt": "P", "active_characters": ["A"]}'
        with patch.object(ai_client, 'generate_text', return_value=mock_json):
            result = ai_client.analyze_scene_for_highlight("text", ["A", "B"])
            assert result["highlight_description"] == "H"
            assert result["active_characters"] == ["A"]

    def test_analyze_scene_for_highlight_exception(self, ai_client):
         with patch.object(ai_client, 'generate_text', side_effect=Exception("Analyze Error")):
            result = ai_client.analyze_scene_for_highlight("text", ["A"])
            assert result["image_prompt"] == "text"
            assert result["active_characters"] == ["A"]

    def test_analyze_scene_for_highlight_invalid_json(self, ai_client):
         with patch.object(ai_client, 'generate_text', return_value="Not JSON"):
            result = ai_client.analyze_scene_for_highlight("text")
            # Should fall back to exception handler inside analyze
            assert result["image_prompt"] == "text"

    def test_generate_image_ref_load_failure(self, ai_client, mock_genai_client, tmp_path):
        mock_instance = mock_genai_client.return_value
        mock_response = MagicMock()
        mock_part = MagicMock()
        mock_part.image.image_bytes = b"img"
        mock_response.parts = [mock_part]
        mock_instance.models.generate_content.return_value = mock_response

        # Pass a non-existent path
        ref_data = [{"path": "/non/existent/path.jpg"}]
        
        output_path = tmp_path / "out.jpg"
        ai_client.generate_image("prompt", reference_images=ref_data, output_path=str(output_path))
        
        # Verify call happened, meaning it didn't crash, just logged warning
        mock_instance.models.generate_content.assert_called()
        # Contents should only have the prompt, no image object
        args, kwargs = mock_instance.models.generate_content.call_args
        assert len(kwargs['contents']) == 1 

    def test_generate_image_as_image_fallback(self, ai_client, mock_genai_client, tmp_path):
        mock_instance = mock_genai_client.return_value
        mock_response = MagicMock()
        
        # Part with no .image but has .as_image()
        mock_part = MagicMock()
        del mock_part.image # Ensure no .image check passes
        
        mock_pil = MagicMock()
        mock_part.as_image.return_value = mock_pil
        
        mock_response.parts = [mock_part]
        mock_instance.models.generate_content.return_value = mock_response

        output_path = tmp_path / "out.jpg"
        ai_client.generate_image("prompt", output_path=str(output_path))
        
        mock_pil.save.assert_called_with(str(output_path))

    def test_generate_image_no_image_returned(self, ai_client, mock_genai_client, tmp_path):
        mock_instance = mock_genai_client.return_value
        mock_response = MagicMock()
        mock_response.parts = [] # No parts
        mock_instance.models.generate_content.return_value = mock_response
        
        with pytest.raises(RuntimeError, match="no images"):
            ai_client.generate_image("prompt", output_path="out.jpg")

    def test_generate_image_exception(self, ai_client, mock_genai_client):
        mock_instance = mock_genai_client.return_value
        mock_instance.models.generate_content.side_effect = Exception("Gen Error")
        
        with pytest.raises(Exception, match="Gen Error"):
            ai_client.generate_image("prompt")

