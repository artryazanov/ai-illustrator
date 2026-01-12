# AI Illustrator

A tool to generate illustrations for stories using Gemini and Imagen.

## Docker Setup

### Prerequisites
- Docker
- Docker Compose

### Setup

1.  **Environment Variables**:
    Copy `.env.example` to `.env` and fill in your API keys.
    ```bash
    cp .env.example .env
    ```

2.  **Build the Image**:
    ```bash
    docker-compose build
    ```

### Usage

To run the generator, you need to provide an input text file.

1.  Place your story text file in a directory (e.g., `data/story.txt`).
2.  Run the container:

    ```bash
    docker-compose run app --text-file data/story.txt --output-dir output/project_name
    ```

    Note: The `docker-compose.yml` mounts the current directory to `/app`, so you can access files relative to the project root.

### Output

The generated illustrations and assets will be saved in the `output` directory (or wherever you specify with `--output-dir`).
