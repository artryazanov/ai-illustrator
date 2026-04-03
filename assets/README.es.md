> 🌐 **Idiomas:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator es una potente herramienta diseñada para generar automáticamente ilustraciones coherentes y de alta calidad para historias utilizando los modelos Gemini de Google tanto para el análisis de texto como para la generación de imágenes. Procesa un archivo de texto de historia, lo analiza para comprender el estilo visual, los personajes y las ubicaciones, y luego genera una secuencia de ilustraciones cinematográficas.

## 🖼️ Demostración

**El cuento de Kolobok**: Para esta demostración, procesamos el clásico cuento de hadas "Kolobok" (El pequeño panecillo redondo). La historia sigue a un panecillo recién horneado que cobra vida, escapa de un anciano y una anciana, y rueda hacia el bosque. A lo largo de su viaje, canta una canción y burla a una liebre, un lobo y un oso, antes de ser finalmente engañado por un astuto zorro.

> **Parámetros de generación:**  
> - **Entrada de historia**: El texto de Kolobok  
> - **Prompt de estilo**: *"cute and whimsical children's book illustration for toddlers"*  
> - **Modelos**: Texto / Validador (`gemini-3.1-pro-preview`), Imagen (`gemini-3.1-flash-image-preview`)
> - **Contexto de resolución**: 512px, Relación de aspecto `1:1`

### Tarjetas de referencia de personajes generadas

<p align="center">
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/2_old_woman.jpeg" width="16%" alt="Old Woman" title="Old Woman" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/3_little_round_bun.jpeg" width="16%" alt="Little Round Bun" title="Little Round Bun" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/4_hare.jpeg" width="16%" alt="Hare" title="Hare" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/5_the_wolf.jpeg" width="16%" alt="The Wolf" title="The Wolf" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/6_bear.jpeg" width="16%" alt="Bear" title="Bear" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/7_the_fox.jpeg" width="16%" alt="The Fox" title="The Fox" />
</p>

### Ilustraciones de escenas generadas

<p align="center">
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/illustrations/1_old_woman_baking_kolobok.jpeg" width="32%" alt="Old Woman Baking" title="Scene 1" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/illustrations/2_rolling_loaf_escapes.jpeg" width="32%" alt="Rolling Loaf Escapes" title="Scene 2" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/illustrations/3_kolobok_meets_hare.jpeg" width="32%" alt="Kolobok Meets Hare" title="Scene 3" />
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/illustrations/4_kolobok_rolls_past_wolf.jpeg" width="32%" alt="Kolobok Rolls Past Wolf" title="Scene 4" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/illustrations/5_kolobok_escapes_bear.jpeg" width="32%" alt="Kolobok Escapes Bear" title="Scene 5" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/illustrations/6_fox_eats_kolobok.jpeg" width="32%" alt="Fox Eats Kolobok" title="Scene 6" />
</p>

## ✨ Características

-   **Detección automática de estilo**: Analiza el texto de la historia para determinar el estilo artístico más apropiado y genera ilustraciones consistentes basadas en ese estilo.
-   **Consistencia de personajes**:
    -   Extrae descripciones de personajes y genera imágenes de referencia de personajes (Cuerpo entero).
    -   Mantiene un catálogo persistente de personajes en `output/data.json` para asegurar que el mismo personaje mantenga un aspecto consistente a lo largo de la historia.
    -   Utiliza el patrón de **Referencias limpias**: Las tarjetas de referencia de personajes se generan estrictamente sobre fondos BLANCOS PUROS aislados para evitar la contaminación del entorno durante la integración de escenas.
    -   Utiliza imágenes de referencia (generación multimodal) para mantener estable la apariencia del personaje en diferentes escenas.
-   **Consistencia de ubicaciones**:
    -   Genera y almacena en caché imágenes de referencia de ubicaciones (Tomas de estilo cinematográfico).
    -   Mantiene un catálogo de ubicaciones en `output/data.json` para reutilizar escenarios.
    -   **Optimización de cuota**: La coincidencia inteligente de ubicaciones asegura que la API solo genere recursos de entorno para ubicaciones estrictamente activas en las escenas de la historia, omitiendo descripciones de fondos no utilizados.
-   **Generación de escenas cinematográficas**:
    -   Divide la historia en escenas lógicas de forma segura utilizando fragmentación semántica (preservando el contexto entre fragmentos).
    -   Paraleliza el renderizado de escenas a través de ThreadPool para una generación más rápida.
    -   Genera un único fotograma cinematográfico cohesivo para cada escena (Relación de aspecto configurable).
    -   Utiliza **Anclaje textual** mapeando explícitamente referencias de múltiples personajes a través de bloques de `MANDATORY VISUAL DETAILS` estructurados estrictamente para evitar que el modelo confunda atuendos o rasgos entre personajes.
-   **Ciclo de control de calidad "LLM-as-a-Judge" y autocorrección**:
    -   Valida de forma nativa las imágenes generadas contra conjuntos de reglas estructurales estrictas (ej., fotograma único, restricciones anatómicas, sin texto, sin bordes).
    -   Si una imagen falla (ej., múltiples ángulos, extremidades adicionales o bordes de encuadre), un prompt de validación estricto activa instantáneamente un bloque de regeneración restringido.
    -   **Editor de estilo inteligente**: Implementa control de calidad programático con IA para validar las descripciones de estilo de texto, evitando falsos positivos (como confundir la palabra prohibida "texto" dentro de la palabra permitida "textura").
    -   **Preservación del contexto**: Los comentarios inyectados anclan fuertemente el modelo para retener la identidad del personaje original y el estilo artístico mientras corrige exclusivamente el error estructural detectado.
    -   **Omisión de filtros de seguridad**: Sanea automáticamente los fallos de control de calidad en bruto a través de un paso intermedio de un LLM "Ingeniero de Prompts". Esto traduce comentarios negativos (como "eliminar marca de agua/firma") en prompts positivos y visualmente claros que omiten de forma segura los filtros de bloqueo del generador de imágenes.
    -   Aplica validación de control de calidad de manera uniforme en **Plantillas de estilo**, **Personajes**, **Ubicaciones** y **Escenas** para mantener una narrativa cohesiva y libre de artefactos.
-   **Salidas estructuradas nativas**:
    -   Reemplaza el frágil análisis de Markdown a JSON con soporte 100% confiable de `response_schema` de Google GenAI mapeado directamente a modelos Pydantic.
-   **Resiliencia de la API**:
    -   Maneja completamente los límites de tasa de la API, tiempos de espera y fallos de carga útil utilizando mecanismos de reintento de retroceso exponencial (`tenacity`).
-   **Soporte para Docker**: Totalmente contenedorizado para facilitar su implementación y ejecución.
-   **Pruebas exhaustivas**: Alta cobertura de pruebas bajo integración continua con Github Actions y Codecov.

## 🛠️ Prerrequisitos

-   **Python 3.12+** (si se ejecuta localmente)
-   **Docker** y **Docker Compose** (recomendado para aislamiento)
-   **Clave API de Google Cloud** con acceso a los modelos Gemini (incluyendo capacidades de generación de imágenes).

## 🚀 Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone git@github.com:artryazanov/ai-illustrator.git
cd ai-illustrator
```

### 2. Configurar el entorno
Copia el archivo de entorno de ejemplo y añade tu clave API.
```bash
cp .env.example .env
```
Abre `.env` y configura tus variables:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # or compatible
VALIDATOR_MODEL_NAME=gemini-3.1-pro-preview # or compatible
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # or specific imagen model
IMAGE_RESOLUTION=1K # Options: 512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # Options: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # Maximum generation attempts during QA loops
```

### 3. Ejecución con Docker (Recomendado)

Construye la imagen de Docker:
```bash
docker-compose build
```

Ejecuta el generador:
1.  Coloca tu archivo de texto de historia en el directorio `data/` (ej., `data/my_story.txt`).
2.  Ejecuta el contenedor:
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *Nota: El directorio `output` se completará con los resultados en tu máquina host.*

### 4. Ejecución local

Crea un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

Instala las dependencias:
```bash
pip install -r requirements.txt
```

Ejecuta la aplicación:
```bash
python main.py --text-file data/my_story.txt --output-dir output/my_project_name
```

## 💡 Uso

### Argumentos de línea de comandos
-   `--text-file`: **(Obligatorio)** Ruta al archivo de texto de entrada que contiene la historia.
-   `--output-dir`: Directorio para guardar los recursos e ilustraciones generadas (por defecto: `output`).
-   `--style-prompt`: Prompt opcional para guiar la detección de estilo inicial (ej., "Anime cyberpunk", "Pintura al óleo").

### Estructura de salida
La herramienta crea un directorio de salida organizado y plano:

```
output/
├── characters/             # Character assets
│   └── 1_character_name.jpeg
├── locations/              # Location assets
│   └── 1_location_name.jpeg
├── illustrations/          # Final Scene Illustrations
│   └── 1_sunny_park_scene.jpeg
├── data.json               # Unified manifest (Style, Characters, Locations, Illustrations)
└── style_templates/        # Generated style base images
    ├── style_reference_fullbody.jpg   # Dynamic character style reference
    └── bg_location.jpg                # Dynamic neutral background for locations
```

### Estructura de `data.json`
El archivo `data.json` sirve como manifiesto central del proyecto.

```json
{
  "style_prompt": "Description of the visual style...",
  "characters": [
    {
      "id": 1,
      "name": "Character Name",
      "original_name": "Original Name from Text",
      "description": "Visual description...",
      "full_body_path": "output/characters/1_character_name.jpeg",
      "generation_prompt": "Full generation prompt used..."
    }
  ],
  "locations": [
    {
      "id": 1,
      "name": "Location Name",
      "original_name": "Original Name from Text",
      "description": "Visual description...",
      "reference_image_path": "output/locations/1_location_name.jpeg",
      "generation_prompt": "Full generation prompt used..."
    }
  ],
  "illustrations": [
    {
      "scene_id": 1,
      "story_segment": "Original text of the scene...",
      "name": "sunny_park_scene",
      "location": {
        "id": 1,
        "name": "Location Name"
      },
      "characters": [
        {
          "id": 1,
          "name": "Character Name",
          "full_body_path": "output/characters/1_character_name.jpeg"
        }
      ],
      "illustration_path": "output/illustrations/1_sunny_park_scene.jpeg",
      "generation_prompt": "Full generation prompt used..."
    }
  ]
}
```

## 🧪 Desarrollo y pruebas

Este proyecto utiliza `pytest` para las pruebas. El conjunto de pruebas cubre los modelos, la configuración, la gestión de recursos, la semántica de división de texto del analizador y el contenedor del cliente de IA. Prueba rigurosamente las estrategias de reserva (fallback), los manejadores de E/S de PIL simulados (mocked), los límites de concurrencia de ThreadPool, los mapeos dinámicos de esquemas y las mecánicas de reintento de retroceso exponencial.

Para ejecutar las pruebas:
```bash
# Activate your virtual environment first
source venv/bin/activate

# Run all tests with coverage reporting
pytest --cov=app --cov-report=term-missing tests/
```

### Mocking (Simulación)
Las pruebas utilizan `unittest.mock` y `pytest-mock` para simular las respuestas de la API de Google GenAI y las operaciones del sistema de archivos, asegurando que las pruebas sean rápidas y no consuman la cuota de la API.

## 🏗️ Estructura del proyecto
-   `main.py`: Punto de entrada y lógica de orquestación.
-   `app/`: Paquete principal.
    -   `config.py`: Configuración y gestión del entorno.
    -   `core/`: Módulos de lógica clave.
        -   `ai_client.py`: Contenedor para el SDK de Google GenAI.
        -   `analyzer.py`: Análisis de la historia (Extracción de escenas/personajes/ubicaciones).
        -   `asset_manager.py`: Gestiona la creación y catalogación de recursos de referencia.
        -   `illustrator.py`: Genera las ilustraciones de las escenas finales.
        -   `models.py`: Modelos de datos de Pydantic.
-   `tests/`: Conjunto de pruebas.

## 📜 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.