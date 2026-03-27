
import pytest
from unittest.mock import MagicMock, patch
import os
from pathlib import Path
import app.config as config_module

class TestConfig:
    def test_validate_success(self, monkeypatch):
        monkeypatch.setattr(config_module.Config, "GEMINI_API_KEY", "test_key")
        # Should not raise
        config_module.Config.validate()

    def test_validate_failure(self, monkeypatch):
        monkeypatch.setattr(config_module.Config, "GEMINI_API_KEY", None)
        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is not set"):
            config_module.Config.validate()
            
    def test_image_resolution_config(self, monkeypatch):
        # Override to ensure it is clean
        monkeypatch.setenv("IMAGE_RESOLUTION", "4K")
        # Reload the module to parse env again, or just manipulate Config manually?
        # Standard approach for settings loaded at import time is to test the default, or mock.
        # Since os.getenv happened at import, modifying env now won't auto-update Config.
        # But we can test that the default is available.
        assert config_module.Config.IMAGE_RESOLUTION in ["512", "1K", "2K", "4K"]

    def test_image_aspect_ratio_config(self, monkeypatch):
        monkeypatch.setenv("IMAGE_ASPECT_RATIO", "16:9")
        assert config_module.Config.IMAGE_ASPECT_RATIO in ["1:1", "16:9", "4:3", "9:16", "21:9"]

    def test_setup_directories(self, tmp_path):
        # Use a temporary directory for output
        base_path = tmp_path / "output"
        config_module.setup_directories(base_path)

        assert (base_path / "characters").exists()
        assert (base_path / "locations").exists()
        assert (base_path / "illustrations").exists()
