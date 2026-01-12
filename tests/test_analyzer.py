
import pytest
from unittest.mock import MagicMock
import json
from app.core.analyzer import StoryAnalyzer
from app.core.models import Scene, Character, Location

@pytest.fixture
def analyzer(mock_genai_client):
    # We can pass the real GenAIClient instance if it uses the mock client internally,
    # or just mock the GenAIClient object passed to Analyzer.
    # Here we mock the GenAIClient object directly for simpler testing of Analyzer logic.
    mock_client = MagicMock()
    return StoryAnalyzer(mock_client)

class TestStoryAnalyzer:
    def test_simple_text_splitter_small(self, analyzer):
        text = "Short text."
        chunks = analyzer.simple_text_splitter(text)
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_simple_text_splitter_large(self, analyzer):
        # Create text larger than chunk size (50k). 
        # Using smaller chunk_size for test would be better but method signature has defaults.
        # We can pass args.
        text = "a" * 100
        chunks = analyzer.simple_text_splitter(text, chunk_size=50, overlap=0)
        assert len(chunks) == 2
        assert chunks[0] == "a" * 50
        assert chunks[1] == "a" * 50

    def test_extract_style(self, analyzer):
        analyzer.ai_client.generate_text.return_value = "Noir Style"
        style = analyzer.extract_style("some text")
        assert style == "Noir Style"

    def test_extract_scenes(self, analyzer):
        # Mock JSON response
        scene_data = [{
            "id": 0, "start_index": 0, "end_index": 10, 
            "time_of_day": "Day", "location_name": "Park",
            "characters_present": ["Alice"], "action_description": "Walking",
            "visual_description": "Sunny park", "mood": "Happy",
            "summary": "Alice in park", "original_text_segment": "Alice walked."
        }]
        analyzer.ai_client.generate_text.return_value = json.dumps(scene_data)
        
        scenes = analyzer.extract_scenes("Alice walked in the park.")
        
        assert len(scenes) == 1
        assert isinstance(scenes[0], Scene)
        assert scenes[0].location_name == "Park"
        # Check re-indexing
        assert scenes[0].id == 1 

    def test_extract_characters(self, analyzer):
        char_data = [{"name": "Alice", "description": "Blonde girl", "original_name": "Alice"}]
        analyzer.ai_client.generate_text.return_value = json.dumps(char_data)
        
        chars = analyzer.extract_characters("text")
        
        assert len(chars) == 1
        assert isinstance(chars[0], Character)
        assert chars[0].name == "Alice"

    def test_extract_locations(self, analyzer):
        loc_data = [{"name": "Park", "description": "Green trees", "original_name": "Park"}]
        analyzer.ai_client.generate_text.return_value = json.dumps(loc_data)
        
        locs = analyzer.extract_locations("text")
        
        assert len(locs) == 1
        assert isinstance(locs[0], Location)
        assert locs[0].name == "Park"

    def test_extract_scenes_failure(self, analyzer):
        analyzer.ai_client.generate_text.return_value = "Not JSON"
        scenes = analyzer.extract_scenes("text")
        assert len(scenes) == 0

    def test_extract_characters_failure(self, analyzer):
        analyzer.ai_client.generate_text.return_value = "Not JSON"
        chars = analyzer.extract_characters("text")
        assert len(chars) == 0

    def test_extract_locations_failure(self, analyzer):
        analyzer.ai_client.generate_text.return_value = "Not JSON"
        locs = analyzer.extract_locations("text")
        assert len(locs) == 0

    def test_extract_style_exception(self, analyzer):
        analyzer.ai_client.generate_text.side_effect = Exception("Err")
        with pytest.raises(Exception, match="Err"):
            analyzer.extract_style("t")

    def test_simple_text_splitter_overlap(self, analyzer):
        # "0123456789"
        # chunk 5, overlap 2
        # 1: 01234
        # 2: 34567
        # 3: 6789 (Wait, real logic without spaces is hard split)
        # Real logic:
        # Start 0, End 5. No space. Chunk "01234". Start=5.
        # Start 5, End 10. No space. Chunk "56789". Start=10.
        text = "0123456789"
        chunks = analyzer.simple_text_splitter(text, chunk_size=5, overlap=2)
        assert len(chunks) == 2
        assert chunks[0] == "01234"
        assert chunks[1] == "56789"
