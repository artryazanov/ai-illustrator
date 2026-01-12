import click
import logging
from pathlib import Path
from dotenv import load_dotenv

from app.config import Config, setup_directories
from app.core.ai_client import GenAIClient
from app.core.analyzer import StoryAnalyzer
from app.core.asset_manager import AssetManager
from app.core.illustrator import StoryIllustrator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@click.command()
@click.option('--text-file', required=True, type=click.Path(exists=True), help='Path to the input text file (story).')
@click.option('--style-prompt', default="", help='Optional initial style preferences.')
@click.option('--output-dir', default="output", help='Directory to save results.')
def main(text_file, style_prompt, output_dir):
    """
    Generates illustrations for a story text file using Gemini/Imagen.
    """
    # 1. Config & Setup
    load_dotenv()
    try:
        Config.validate()
    except ValueError as e:
        logger.error(str(e))
        return

    output_path = Path(output_dir)
    setup_directories(output_path)

    # Read Text
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()

    logger.info(f"Loaded text file: {text_file} ({len(text_content)} chars)")

    # 2. Initialize Core Components
    ai_client = GenAIClient()
    analyzer = StoryAnalyzer(ai_client)
    asset_manager = AssetManager(ai_client, output_path)
    illustrator = StoryIllustrator(ai_client, asset_manager, output_path)

    # 3. Analyze Style
    logger.info("Analyzing text for style...")
    # We use the first chunk or summary for style if text is huge
    style_sample = text_content[:5000]
    detected_style = analyzer.extract_style(style_sample, style_prompt)
    logger.info(f"Detected Style: {detected_style}")

    # Prepare global templates (Characters 9:16 and Locations 16:9)
    # Swapped order as requested: Locations first, then Style
    asset_manager.prepare_location_templates(detected_style)
    asset_manager.prepare_style_templates(detected_style)

    # 4. Analyze Scenes (Splitting first to handle large texts in chunks)
    logger.info("Splitting text into scenes...")
    scenes = analyzer.extract_scenes(text_content)
    logger.info(f"Identified {len(scenes)} scenes.")

    # 5. Iterative Generation Loop
    # We iterate through scene groups (chunks) or scene-by-scene to extract entities
    # and generate assets dynamically as the story progresses.

    logger.info("Starting processing loop...")

    for scene in scenes:
        logger.info(f"Processing Scene {scene.id} at {scene.location_name}")

        # Analyze the scene text for NEW entities not yet in our asset manager
        # Optimization: We check if the entities mentioned in scene metadata are known.
        # However, to be thorough as requested ("Extract ... first thing when processing chunk"),
        # we scan the text of the scene (or the chunk it came from).
        # Since 'scenes' are granular, we can scan the scene text.

        scene_text = scene.original_text_segment

        # Extract Characters in this scene
        chars_in_scene = analyzer.extract_characters(scene_text)
        asset_manager.generate_character_assets(chars_in_scene, detected_style)

        # Extract Locations in this scene
        locs_in_scene = analyzer.extract_locations(scene_text)
        asset_manager.generate_location_assets(locs_in_scene, detected_style)

        # Generate Illustration
        illustrator.illustrate_scenes([scene], detected_style)

    logger.info("Job Complete! Check the output directory.")

if __name__ == '__main__':
    main()
