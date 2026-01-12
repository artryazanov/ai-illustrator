
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

    def test_generate_image_with_ref(self, ai_client, mock_genai_client, tmp_path):
        # Create a dummy ref image
        ref_path = tmp_path / "ref.jpg"
        ref_path.write_bytes(b"ref_bytes")
        
        # Mock Image.open
        with patch("PIL.Image.open") as mock_open:
            mock_open.return_value = "ParsedImage"

            # Setup mock response
            mock_instance = mock_genai_client.return_value
            mock_response = MagicMock()
            mock_part = MagicMock()
            mock_part.image.image_bytes = b"result_bytes"
            mock_response.parts = [mock_part]
            mock_instance.models.generate_content.return_value = mock_response
            
            output_path = tmp_path / "result.jpg"
            
            ref_data = [{
                "path": str(ref_path),
                "purpose": "Test Purpose",
                "usage": "Test Usage"
            }]
            
            ai_client.generate_image("prompt", reference_images=ref_data, output_path=str(output_path))
            
            # Check if contents list includes the image
            args, kwargs = mock_instance.models.generate_content.call_args
            contents = kwargs['contents']
            
            # Validate contents structure: [PromptString, ImageObject]
            assert len(contents) == 2 
            
            # 1. Validate Prompt Augmentation
            assert "prompt" in contents[0]
            assert "Reference Images Context" in contents[0]
            assert "File: ref.jpg" in contents[0]
            assert "Purpose: Test Purpose" in contents[0]
            
            # 2. Validate Image Passing
            assert contents[1] == "ParsedImage"

