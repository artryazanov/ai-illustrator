
import pytest
import json
from unittest.mock import MagicMock
from pathlib import Path
from app.core.asset_manager import AssetManager
from app.core.models import Character, Location

@pytest.fixture
def mock_wrapper_client():
    from app.core.ai_client import GenAIClient
    client = MagicMock(spec=GenAIClient)
    return client

@pytest.fixture
def asset_manager(mock_wrapper_client, tmp_path):
    output_dir = tmp_path / "output"
    return AssetManager(mock_wrapper_client, output_dir)

class TestSemanticDeduplication:

    def test_semantic_match_character_found(self, asset_manager):
        # Setup existing character
        existing = Character(id=1, name="John Doe", description="A tall man with a hat.", full_body_path="path/to/img.jpg")
        asset_manager.characters["John Doe"] = existing
        
        # New character with different name but similar concept
        new_char = Character(name="The Stranger", description="Tall guy wearing a fedora.")

        # Mock AI response
        response_json = json.dumps({"match_id": 1, "reason": "Evaluated as same person."})
        asset_manager.ai_client.generate_text.return_value = response_json

        # Run check directly
        match = asset_manager._check_existing_character_semantic(new_char)
        
        assert match is not None
        assert match.id == 1
        assert match.name == "John Doe"

    def test_semantic_match_character_not_found(self, asset_manager):
        existing = Character(id=1, name="John Doe", description="A tall man.")
        asset_manager.characters["John Doe"] = existing
        
        new_char = Character(name="Jane Doe", description="A short woman.")

        asset_manager.ai_client.generate_text.return_value = json.dumps({"match_id": None, "reason": "Different gender."})

        match = asset_manager._check_existing_character_semantic(new_char)
        assert match is None

    def test_generate_character_assets_uses_semantic_link(self, asset_manager):
        # Existing
        existing = Character(id=5, name="King", description="The king.", full_body_path="king.jpg")
        asset_manager.characters["King"] = existing
        
        # New alias
        new_char = Character(name="His Majesty", description="The ruler of the land.")
        
        # Mock semantic match
        asset_manager.ai_client.generate_text.return_value = json.dumps({"match_id": 5, "reason": "Same person"})
        
        # Call generate
        asset_manager.generate_character_assets([new_char], "style")
        
        # Verify
        assert new_char.id == 5
        assert new_char.full_body_path == "king.jpg"
        # Logic should NOT generate new image
        asset_manager.ai_client.generate_image.assert_not_called()
        # Should be added to catalog
        assert "His Majesty" in asset_manager.characters
        assert asset_manager.characters["His Majesty"].id == 5

    def test_semantic_match_location_found(self, asset_manager):
        existing = Location(id=10, name="Old Barn", description="Red wood structure.", reference_image_path="barn.jpg")
        asset_manager.locations["Old Barn"] = existing
        
        new_loc = Location(name="The Barn", description="Wooden red building.")
        
        asset_manager.ai_client.generate_text.return_value = json.dumps({"match_id": 10, "reason": "Refers to same building"})
        
        match = asset_manager._check_existing_location_semantic(new_loc)
        assert match.id == 10

    def test_generate_location_assets_uses_semantic_link(self, asset_manager):
        existing = Location(id=20, name="City Park", description="Green grass.", reference_image_path="park.jpg")
        asset_manager.locations["City Park"] = existing
        
        new_loc = Location(name="Public Park", description="Park with grass.")
        
        asset_manager.ai_client.generate_text.return_value = json.dumps({"match_id": 20, "reason": "Same place"})
        
        asset_manager.generate_location_assets([new_loc], "style")
        
        assert new_loc.id == 20
        assert new_loc.reference_image_path == "park.jpg"
        asset_manager.ai_client.generate_image.assert_not_called()
        assert "Public Park" in asset_manager.locations

    def test_semantic_check_empty_db(self, asset_manager):
        new_char = Character(name="Solo", description="Solo")
        match = asset_manager._check_existing_character_semantic(new_char)
        assert match is None
