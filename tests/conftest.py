
import pytest
from unittest.mock import MagicMock
import sys
import os

# Add project root to sys.path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_genai_client(mocker):
    """Fixture to mock the Google GenAI Client."""
    mock_client = mocker.patch('google.genai.Client')
    return mock_client

@pytest.fixture
def mock_env(monkeypatch):
    """Fixture to mock environment variables."""
    monkeypatch.setenv("GOOGLE_API_KEY", "fake_key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")
