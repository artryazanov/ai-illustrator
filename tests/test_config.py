
import pytest
from unittest.mock import MagicMock, patch
import os
from pathlib import Path
import illustration_gen.config as config_module

class TestConfig:
    def test_validate_success(self, monkeypatch):
        monkeypatch.setattr(config_module.Config, "GEMINI_API_KEY", "test_key")
        # Should not raise
        config_module.Config.validate()

    def test_validate_failure(self, monkeypatch):
        monkeypatch.setattr(config_module.Config, "GEMINI_API_KEY", None)
        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is not set"):
            config_module.Config.validate()

    def test_setup_directories(self, tmp_path):
        # Use a temporary directory for output
        base_path = tmp_path / "output"
        config_module.setup_directories(base_path)

        assert (base_path / "characters").exists()
        assert (base_path / "locations").exists()
        assert (base_path / "illustrations").exists()
