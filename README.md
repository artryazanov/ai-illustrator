# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Docker Build](https://github.com/artryazanov/ai-illustrator/actions/workflows/docker.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/docker.yml)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator is a powerful tool designed to automatically generate consistent, high-quality illustrations for stories using Google's Gemini models for both text analysis and image generation. It processes a story text file, analyzes it to understand the visual style, characters, and locations, and then generates a sequence of cinematic illustrations.

## ✨ Features

-   **Automatic Style Detection**: Analyzes the story text to determine the most appropriate art style and generates consistent illustrations based on that style.
-   **Character Consistency**:
    -   Extracts character descriptions and generates reference character images (Full Body).
    -   Maintains a persistent catalog of characters in `output/data.json` to ensure the same character looks consistent throughout the story.
    -   Uses reference images (multimodal generation) to keep character appearance stable across different scenes.
-   **Location Consistency**:
    -   Generates and caches location reference images (16:9 cinematic shots).
    -   Maintains a location catalog in `output/data.json` to reuse settings.
-   **Cinematic Scene Generation**:
    -   Splits the story into logical scenes.
    -   Generates a single, cohesive cinematic frame for each scene (16:9 aspect ratio).
    -   Enforces strict negative constraints to prevent comic-book layouts, text, or split screens.
    -   Uses full-body character references to maintain consistency across scenes.
-   **Docker Support**: Fully containerized for easy deployment and execution.
-   **Comprehensive Testing**: Includes a full suite of unit and integration-like tests using `pytest`.

## 🛠️ Prerequisites

-   **Python 3.10+** (if running locally)
-   **Docker** & **Docker Compose** (recommended for isolation)
-   **Google Cloud API Key** with access to Gemini models (including image generation capabilities).

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-illustrator
```

### 2. Configure Environment
Copy the example environment file and add your API key.
```bash
cp .env.example .env
```
Open `.env` and set your variables:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3-pro-preview # or compatible
IMAGE_MODEL_NAME=gemini-3-pro-image-preview # or specific imagen model
```

### 3. Running with Docker (Recommended)

Build the Docker image:
```bash
docker-compose build
```

Run the generator:
1.  Place your story text file in the `data/` directory (e.g., `data/my_story.txt`).
2.  Execute the container:
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *Note: The `output` directory will be populated with the results on your host machine.*

### 4. Running Locally

Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python main.py --text-file data/my_story.txt --output-dir output/my_project_name
```

## 💡 Usage

### Command Line Arguments
-   `--text-file`: **(Required)** Path to the input text file containing the story.
-   `--output-dir`: Directory to save generated assets and illustrations (default: `output`).
-   `--style-prompt`: Optional prompt to guide the initial style detection (e.g., "Cyberpunk anime", "Oil painting").

### Output Structure
The tool creates an organized output directory:

```
output/
├── characters/             # Character assets
│   └── Character_Name/     # Specific character folder
│       └── card_full.jpg   # Full body reference
├── locations/              # Location assets
│   └── Location_Name/
│       └── ref_01.jpg      # Location reference
├── illustrations/          # Final Scene Illustrations
│   ├── 001_Location_Name/
│   │   └── illustration.jpg
│   └── ...
├── data.json               # Unified manifest (Style, Characters, Locations, Illustrations)
└── style_templates/        # Generated style base images
```

### `data.json` Structure
The `data.json` file serves as the central manifest for the project.

```json
{
  "style_prompt": "Description of the visual style...",
  "characters": [
    {
      "name": "Character Name",
      "original_name": "Original Name from Text",
      "description": "Visual description...",
      "full_body_path": "output/characters/Name/card_full.jpg"
    }
  ],
  "locations": [
    {
      "name": "Location Name",
      "original_name": "Original Name from Text",
      "description": "Visual description...",
      "reference_image_path": "output/locations/Name/ref_01.jpg"
    }
  ],
  "illustrations": [
    {
      "scene_id": 1,
      "story_segment": "Original text of the scene...",
      "location": {
        "name": "Location Name",
        "path": "output/locations/Name/ref_01.jpg"
      },
      "characters": [
        {
          "name": "Character Name",
          "full_body_path": "output/characters/Name/card_full.jpg"
        }
      ],
      "illustration_path": "illustrations/001_Loc/illustration.jpg",
      "folder": "001_Location_Name"
    }
  ]
}
```

## 🧪 Development & Testing

This project uses `pytest` for testing. The test suite covers models, configuration, asset management, and the AI client wrapper.

To run tests:
```bash
# Activate your virtual environment first
source venv/bin/activate

# Run all tests
pytest tests

# Run with verbose output
pytest -v tests
```

### Mocking
The tests use `unittest.mock` and `pytest-mock` to simulate Google GenAI API responses and filesystem operations, ensuring that tests are fast and do not consume API quota.

## 🏗️ Project Structure
-   `main.py`: Entry point and orchestration logic.
-   `app/`: Core package.
    -   `config.py`: Configuration and environment management.
    -   `core/`: Key logic modules.
        -   `ai_client.py`: Wrapper for Google GenAI SDK.
        -   `analyzer.py`: Story analysis (Scene/Character/Location extraction).
        -   `asset_manager.py`: Manages creation and cataloging of reference assets.
        -   `illustrator.py`: Generates the final scene illustrations.
        -   `models.py`: Pydantic data models.
-   `tests/`: Test suite.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
