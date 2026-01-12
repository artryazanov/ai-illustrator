
import pytest
from unittest.mock import MagicMock, patch
from app.core.ai_client import GenAIClient
import json

@pytest.fixture
def mock_genai_client():
    with patch('app.core.ai_client.genai.Client') as mock_client:
        client = GenAIClient()
        # Mock the underlying client's generate_content method
        client.client.models.generate_content = MagicMock()
        yield client

def test_analyze_scene_for_highlight_success(mock_genai_client):
    # Setup mock response
    expected_response = {
        "highlight_description": "The hero draws their sword.",
        "image_prompt": "A close up of a shining sword being drawn from a scabbard."
    }
    
    mock_response = MagicMock()
    mock_response.text = json.dumps(expected_response)
    mock_genai_client.client.models.generate_content.return_value = mock_response

    # Call method
    scene_text = "The room was quiet. Suddenly, the hero drew their sword. Everyone gasped."
    result = mock_genai_client.analyze_scene_for_highlight(scene_text)

    # Assertions
    assert result == expected_response
    assert "highlight_description" in result
    assert "image_prompt" in result
    
    # Verify the prompt contained the instructions
    call_args = mock_genai_client.client.models.generate_content.call_args
    assert call_args is not None
    prompt_sent = call_args.kwargs['contents']
    assert "Analyze the following scene text" in prompt_sent
    assert scene_text in prompt_sent

def test_analyze_scene_for_highlight_json_cleanup(mock_genai_client):
    # Setup mock response with markdown blocks
    json_content = '{"highlight_description": "test", "image_prompt": "test prompt"}'
    markdown_response = f'```json\n{json_content}\n```'
    
    mock_response = MagicMock()
    mock_response.text = markdown_response
    mock_genai_client.client.models.generate_content.return_value = mock_response

    # Call method
    result = mock_genai_client.analyze_scene_for_highlight("text")

    # Assertions
    assert result["highlight_description"] == "test"

def test_analyze_scene_for_highlight_failure(mock_genai_client):
    # Setup mock to raise exception
    mock_genai_client.client.models.generate_content.side_effect = Exception("API Error")

    # Call method
    scene_text = "Some text"
    result = mock_genai_client.analyze_scene_for_highlight(scene_text)

    # Assertions should return fallback
    assert result["image_prompt"] == scene_text
    assert "Fallback" in result["highlight_description"]
    assert result["active_characters"] == []

def test_analyze_scene_for_highlight_active_characters(mock_genai_client):
    # Setup mock response with active characters
    expected_response = {
        "highlight_description": "A conversation.",
        "image_prompt": "Two people talking.",
        "active_characters": ["Alice", "Bob"]
    }
    
    # Mock return value
    mock_response = MagicMock()
    mock_response.text = json.dumps(expected_response)
    mock_genai_client.client.models.generate_content.return_value = mock_response

    # Call method with available characters
    available = ["Alice", "Bob", "Charlie", "Dave"]
    result = mock_genai_client.analyze_scene_for_highlight("scene text", available_characters=available)

    # Assertions
    assert "Alice" in result["active_characters"]
    assert "Bob" in result["active_characters"]
    assert "Charlie" not in result["active_characters"]
    
    # Check prompt included instructions
    call_args = mock_genai_client.client.models.generate_content.call_args
    prompt_sent = call_args.kwargs['contents']
    assert "The following characters are present" in prompt_sent
    assert "Identify EXACTLY which of these characters" in prompt_sent

def test_analyze_scene_for_highlight_hallucination_filtering(mock_genai_client):
    # Setup mock response with hallucinated character
    expected_response = {
        "active_characters": ["Alice", "Gandalf"] # Gandalf is not in available list
    }
    
    mock_response = MagicMock()
    mock_response.text = json.dumps(expected_response)
    mock_genai_client.client.models.generate_content.return_value = mock_response

    # Call method
    available = ["Alice", "Bob"]
    result = mock_genai_client.analyze_scene_for_highlight("text", available_characters=available)

    # Assertions - Gandalf should be filtered out
    assert "Alice" in result["active_characters"]
    assert "Gandalf" not in result["active_characters"]
