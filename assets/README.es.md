> 🌐 **Idiomas:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator es una potente herramienta diseñada para generar automáticamente ilustraciones consistentes y de alta calidad para historias, utilizando los modelos Gemini de Google tanto para el análisis de texto como para la generación de imágenes. Procesa un archivo de texto de una historia, lo analiza para comprender el estilo visual, los personajes y las ubicaciones, y luego genera una secuencia de ilustraciones cinematográficas.

## 🖼️ Demostración

**El Cuento de Kolobok**: Para esta demostración, procesamos el clásico cuento de hadas "Kolobok" (El Pequeño Panecillo Redondo). La historia sigue a un panecillo recién horneado que cobra vida, escapa de un anciano y una anciana, y rueda hacia el bosque. A lo largo de su viaje, canta una canción y burla a una liebre, un lobo y un oso, antes de ser finalmente engañado por un astuto zorro.

> **Parámetros de Generación:**  
> - **Entrada de Historia**: El texto de Kolobok  
> - **Prompt de Estilo**: *"ilustración linda y caprichosa de libro infantil para niños pequeños"*  
> - **Modelos**: Texto / Validador (`gemini-3.1-pro-preview`), Imagen (`gemini-3.1-flash-image-preview`)
> - **Contexto de Resolución**: 512px, Relación de Aspecto `1:1`

### Tarjetas de Referencia de Personajes Generadas

<p align="center">
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/2_old_woman.jpeg" width="16%" alt="Old Woman" title="Old Woman" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/3_little_round_bun.jpeg" width="16%" alt="Little Round Bun" title="Little Round Bun" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/4_hare.jpeg" width="16%" alt="Hare" title="Hare" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/5_the_wolf.jpeg" width="16%" alt="The Wolf" title="The Wolf" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/6_bear.jpeg" width="16%" alt="Bear" title="Bear" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/7_the_fox.jpeg" width="16%" alt="The Fox" title="The Fox" />
</p>

### Ilustraciones de Escenas Generadas

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

-   **Detección Automática de Estilo**: Analiza el texto de la historia para determinar el estilo artístico más apropiado y genera ilustraciones consistentes basadas en dicho estilo.
-   **Consistencia de Personajes**:
    -   Extrae descripciones de personajes y genera imágenes de referencia de los mismos (Cuerpo Entero).
    -   Mantiene un catálogo persistente de personajes en `output/data.json` para asegurar que el mismo personaje se vea de manera consistente a lo largo de toda la historia.
    -   Utiliza el patrón de **Referencias Limpias**: las tarjetas de referencia de personajes se generan estrictamente sobre fondos BLANCO PURO aislados para evitar la mezcla de elementos del entorno durante la integración de escenas.
    -   Utiliza imágenes de referencia (generación multimodal) para mantener estable la apariencia del personaje en diferentes escenas.
-   **Consistencia de Ubicaciones**:
    -   Genera y almacena en caché imágenes de referencia de ubicaciones (Tomas de estilo cinematográfico).
    -   Mantiene un catálogo de ubicaciones en `output/data.json` para reutilizar los escenarios.
    -   **Optimización de Cuota**: El emparejamiento inteligente de ubicaciones asegura que la API solo genere recursos de entorno para aquellas ubicaciones que estén estrictamente activas en las escenas de la historia, omitiendo descripciones de fondos no utilizados.
-   **Generación de Escenas Cinematográficas**:
    -   Divide la historia en escenas lógicas de forma segura utilizando Fragmentación Semántica (conservando el contexto entre fragmentos).
    -   Paraleliza el renderizado de escenas a través de ThreadPool para una generación más rápida.
    -   Genera un único fotograma cinematográfico cohesivo para cada escena (Relación de aspecto configurable).
    -   Utiliza el **Anclaje Textual** mapeando explícitamente referencias de múltiples personajes a través de bloques `MANDATORY VISUAL DETAILS` (DETALLES VISUALES OBLIGATORIOS) estrictamente estructurados para evitar que el modelo confunda vestimentas o rasgos entre personajes.
-   **Bucle de Control de Calidad (QA) con LLM como Juez y Autocorrección**:
    -   Valida nativamente las imágenes generadas frente a conjuntos de reglas estructurales estrictas (ej. Un Solo Fotograma, restricciones anatómicas, Sin Texto, Sin Bordes).
    -   Si una imagen falla (ej. múltiples ángulos, extremidades extra, o bordes de encuadre), un prompt estricto de validación desencadena instantáneamente un bloque de regeneración restringido.
    -   **Editor de Estilo Inteligente**: Implementa QA mediante IA programática para validar las descripciones de estilo de texto, previniendo alertas de falsos positivos (como confundir la palabra prohibida "texto" dentro de la palabra permitida "textura").
    -   **Preservación del Contexto**: La retroalimentación inyectada ancla fuertemente al modelo para retener la identidad original del personaje y el estilo artístico, corrigiendo exclusivamente el error estructural señalado.
    -   **Evasión de Filtros de Seguridad**: Sanea automáticamente los fallos brutos de QA a través de un paso intermedio de LLM de tipo "Ingeniero de Prompts". Esto traduce la retroalimentación negativa (como "eliminar marca de agua/firma") en prompts positivos y visualmente claros que eluden de manera segura los filtros de bloqueo del generador de imágenes.
    -   Aplica la validación de QA de manera uniforme en **Plantillas de Estilo**, **Personajes**, **Ubicaciones** y **Escenas** para mantener una narrativa cohesiva y libre de artefactos.
-   **Salidas Estructuradas Nativas**:
    -   Reemplaza el frágil análisis de markdown-JSON con un soporte 100% fiable de `response_schema` de Google GenAI, mapeado directamente a modelos de Pydantic.
-   **Resiliencia de la API**:
    -   Maneja completamente los límites de tasa de la API, tiempos de espera y fallos de carga útil utilizando mecanismos de reintento de retroceso exponencial (`tenacity`).
-   **Soporte de Docker**: Completamente en contenedores para facilitar su despliegue y ejecución.
-   **Pruebas Exhaustivas**: Alta cobertura de pruebas bajo integración continua con Github Actions y Codecov.

## 🛠️ Requisitos Previos

-   **Python 3.12+** (si se ejecuta localmente)
-   **Docker** y **Docker Compose** (recomendado para aislamiento)
-   **Clave API de Google Cloud** con acceso a los modelos Gemini (incluyendo capacidades de generación de imágenes).

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone git@github.com:artryazanov/ai-illustrator.git
cd ai-illustrator
```

### 2. Configurar el Entorno
Copie el archivo de entorno de ejemplo y añada su clave API.
```bash
cp .env.example .env
```
Abra `.env` y configure sus variables:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # or compatible
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # or specific imagen model
IMAGE_RESOLUTION=1K # Options: 512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # Options: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # Maximum generation attempts during QA loops
```

### 3. Ejecutar con Docker (Recomendado)

Construir la imagen de Docker:
```bash
docker-compose build
```

Ejecutar el generador:
1.  Coloque su archivo de texto con la historia en el directorio `data/` (ej., `data/my_story.txt`).
2.  Ejecute el contenedor:
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *Nota: El directorio `output` se poblará con los resultados en su máquina host.*

### 4. Ejecutar Localmente

Crear un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar las dependencias:
```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:
```bash
python main.py --text-file data/my_story.txt --output-dir output/my_project_name
```

## 💡 Uso

### Argumentos de Línea de Comandos
-   `--text-file`: **(Requerido)** Ruta al archivo de texto de entrada que contiene la historia.
-   `--output-dir`: Directorio para guardar los recursos e ilustraciones generadas (predeterminado: `output`).
-   `--style-prompt`: Prompt opcional para guiar la detección de estilo inicial (ej., "Cyberpunk anime", "Pintura al óleo").

### Estructura de Salida
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

## 🧪 Desarrollo y Pruebas

Este proyecto utiliza `pytest` para las pruebas. La suite de pruebas cubre modelos, configuración, gestión de recursos, semántica de división de texto del analizador, y el envoltorio del cliente de IA. Prueba rigurosamente las estrategias de respaldo (fallbacks), manejadores de IO de PIL simulados, límites de concurrencia de ThreadPool, mapeos dinámicos de esquemas y mecánicas de reintento con retroceso exponencial.

Para ejecutar las pruebas:
```bash
# Activate your virtual environment first
source venv/bin/activate

# Run all tests with coverage reporting
pytest --cov=app --cov-report=term-missing tests/
```

### Simulaciones (Mocking)
Las pruebas utilizan `unittest.mock` y `pytest-mock` para simular las respuestas de la API de Google GenAI y las operaciones del sistema de archivos, garantizando que las pruebas sean rápidas y no consuman la cuota de la API.

## 🏗️ Estructura del Proyecto
-   `main.py`: Punto de entrada y lógica de orquestación.
-   `app/`: Paquete principal.
    -   `config.py`: Configuración y gestión del entorno.
    -   `core/`: Módulos de lógica clave.
        -   `ai_client.py`: Envoltorio para el SDK de Google GenAI.
        -   `analyzer.py`: Análisis de la historia (Extracción de Escenas/Personajes/Ubicaciones).
        -   `asset_manager.py`: Gestiona la creación y catalogación de recursos de referencia.
        -   `illustrator.py`: Genera las ilustraciones finales de las escenas.
        -   `models.py`: Modelos de datos de Pydantic.
-   `tests/`: Suite de pruebas.

## 📜 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulte el archivo [LICENSE](LICENSE) para más detalles.