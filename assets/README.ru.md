> 🌐 **Языки:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator — это мощный инструмент, предназначенный для автоматической генерации последовательных, высококачественных иллюстраций к рассказам с использованием моделей Google Gemini как для анализа текста, так и для генерации изображений. Он обрабатывает текстовый файл истории, анализирует его для понимания визуального стиля, персонажей и локаций, а затем генерирует серию кинематографических иллюстраций.

## 🖼️ Демонстрация

**Сказка о Колобке**: Для этой демонстрации мы обработали классическую сказку «Колобок». История рассказывает о свежеиспеченном колобке, который оживает, убегает от деда и бабы и катится в лес. Во время своего путешествия он поет песенку и перехитряет зайца, волка и медведя, прежде чем в конце концов оказывается обманутым хитрой лисой.

> **Параметры генерации:**  
> - **Входной текст**: Текст сказки «Колобок»  
> - **Промпт стиля**: *"милые и сказочные детские книжные иллюстрации для малышей"*  
> - **Модели**: Текст / Валидатор (`gemini-3.1-pro-preview`), Изображения (`gemini-3.1-flash-image-preview`)
> - **Разрешение и формат**: 512px, соотношение сторон `1:1`

### Сгенерированные референсы персонажей

<p align="center">
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/2_old_woman.jpeg" width="16%" alt="Old Woman" title="Old Woman" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/3_little_round_bun.jpeg" width="16%" alt="Little Round Bun" title="Little Round Bun" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/4_hare.jpeg" width="16%" alt="Hare" title="Hare" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/5_the_wolf.jpeg" width="16%" alt="The Wolf" title="The Wolf" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/6_bear.jpeg" width="16%" alt="Bear" title="Bear" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/7_the_fox.jpeg" width="16%" alt="The Fox" title="The Fox" />
</p>

### Сгенерированные иллюстрации сцен

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

## ✨ Возможности

-   **Автоматическое определение стиля**: Анализирует текст истории для определения наиболее подходящего художественного стиля и генерирует согласованные иллюстрации на его основе.
-   **Согласованность персонажей**:
    -   Извлекает описания персонажей и генерирует эталонные изображения (в полный рост).
    -   Поддерживает постоянный каталог персонажей в `output/data.json`, чтобы гарантировать одинаковый внешний вид персонажа на протяжении всей истории.
    -   Использует паттерн **Чистых референсов (Clean References)**: карточки персонажей генерируются строго на изолированном ЧИСТО-БЕЛОМ фоне, чтобы предотвратить смешивание с окружением при интеграции в сцену.
    -   Использует эталонные изображения (мультимодальная генерация) для сохранения стабильного вида персонажей в разных сценах.
-   **Согласованность локаций**:
    -   Генерирует и кэширует эталонные изображения локаций (в кинематографическом стиле).
    -   Поддерживает каталог локаций в `output/data.json` для повторного использования окружения.
    -   **Оптимизация квот**: Умное сопоставление локаций гарантирует, что API генерирует ассеты окружения только для тех локаций, которые активно задействованы в сценах истории, пропуская неиспользуемые фоновые описания.
-   **Генерация кинематографических сцен**:
    -   Надежно разбивает историю на логические сцены с использованием семантического чанкинга (с сохранением контекста между фрагментами).
    -   Распараллеливает рендеринг сцен через ThreadPool для ускорения генерации.
    -   Создает единый, целостный кинематографический кадр для каждой сцены (с настраиваемым соотношением сторон).
    -   Использует **Текстовую привязку (Textual Anchoring)**: явным образом сопоставляет мульти-персонажные референсы через строго структурированные блоки `MANDATORY VISUAL DETAILS`, чтобы модель не перепутала одежду или черты лица между персонажами.
-   **QA-цикл LLM в роли судьи и самокоррекция**:
    -   Нативно проверяет сгенерированные изображения на соответствие строгим структурным правилам (например, один кадр, ограничения анатомии, отсутствие текста и рамок).
    -   Если изображение не проходит проверку (например, несколько ракурсов, лишние конечности или рамки), строгий промпт валидации мгновенно запускает цикл перегенерации с заданными ограничениями.
    -   **Умный редактор стиля**: Реализует программный ИИ QA для проверки описаний текстовых стилей, предотвращая ложные срабатывания (например, путаницу запрещенного слова "text" внутри разрешенного слова "texture").
    -   **Сохранение контекста**: Внедренная обратная связь строго привязывает модель к сохранению оригинальной идентичности персонажа и художественного стиля, фокусируясь исключительно на исправлении отмеченной структурной ошибки.
    -   **Обход фильтров безопасности**: Автоматически очищает сырые отказы QA через промежуточный проход LLM "Промпт-инженера". Это переводит негативный фидбек (например, "удалить водяной знак/подпись") в позитивные, визуально четкие промпты, которые безопасно обходят блокирующие фильтры генераторов изображений.
    -   Применяет QA-валидацию единообразно к **Шаблонам стиля**, **Персонажам**, **Локациям** и **Сценам** для поддержания целостного повествования без артефактов.
-   **Нативные структурированные ответы**:
    -   Заменяет хрупкий парсинг markdown-JSON на 100% надежную поддержку Google GenAI `response_schema`, напрямую связанную с моделями Pydantic.
-   **Устойчивость API**:
    -   Полностью обрабатывает лимиты запросов API, таймауты и сбои полезной нагрузки, используя механизмы повторных попыток с экспоненциальной задержкой (`tenacity`).
-   **Поддержка Docker**: Полностью контейнеризировано для легкого развертывания и запуска.
-   **Комплексное тестирование**: Высокое покрытие тестами в условиях непрерывной интеграции с Github Actions и Codecov.

## 🛠️ Требования

-   **Python 3.12+** (при локальном запуске)
-   **Docker** и **Docker Compose** (рекомендуется для изоляции)
-   **API-ключ Google Cloud** с доступом к моделям Gemini (включая возможности генерации изображений).

## 🚀 Установка и настройка

### 1. Клонирование репозитория
```bash
git clone git@github.com:artryazanov/ai-illustrator.git
cd ai-illustrator
```

### 2. Настройка окружения
Скопируйте пример файла конфигурации окружения и добавьте свой API-ключ.
```bash
cp .env.example .env
```
Откройте `.env` и настройте переменные:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # или совместимая
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # или конкретная модель imagen
IMAGE_RESOLUTION=1K # Варианты: 512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # Варианты: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # Максимальное количество попыток генерации в циклах QA
```

### 3. Запуск с помощью Docker (Рекомендуется)

Сборка Docker-образа:
```bash
docker-compose build
```

Запуск генератора:
1.  Поместите текстовый файл с вашей историей в директорию `data/` (например, `data/my_story.txt`).
2.  Запустите контейнер:
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *Примечание: Директория `output` с результатами работы будет создана на вашей хост-машине.*

### 4. Локальный запуск

Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```

Установите зависимости:
```bash
pip install -r requirements.txt
```

Запустите приложение:
```bash
python main.py --text-file data/my_story.txt --output-dir output/my_project_name
```

## 💡 Использование

### Аргументы командной строки
-   `--text-file`: **(Обязательно)** Путь к входному текстовому файлу, содержащему историю.
-   `--output-dir`: Директория для сохранения сгенерированных ассетов и иллюстраций (по умолчанию: `output`).
-   `--style-prompt`: Необязательный промпт для указания начального стиля (например, "Киберпанк аниме", "Картина маслом").

### Структура вывода
Инструмент создает организованную, плоскую структуру выходной директории:

```
output/
├── characters/             # Ассеты персонажей
│   └── 1_character_name.jpeg
├── locations/              # Ассеты локаций
│   └── 1_location_name.jpeg
├── illustrations/          # Итоговые иллюстрации сцен
│   └── 1_sunny_park_scene.jpeg
├── data.json               # Единый манифест (Стиль, Персонажи, Локации, Иллюстрации)
└── style_templates/        # Сгенерированные базовые изображения стиля
    ├── style_reference_fullbody.jpg   # Динамический референс стиля персонажа
    └── bg_location.jpg                # Динамический нейтральный фон для локаций
```

### Структура `data.json`
Файл `data.json` служит центральным манифестом проекта.

```json
{
  "style_prompt": "Описание визуального стиля...",
  "characters": [
    {
      "id": 1,
      "name": "Имя персонажа",
      "original_name": "Оригинальное имя из текста",
      "description": "Визуальное описание...",
      "full_body_path": "output/characters/1_character_name.jpeg",
      "generation_prompt": "Полный использованный промпт генерации..."
    }
  ],
  "locations": [
    {
      "id": 1,
      "name": "Название локации",
      "original_name": "Оригинальное имя из текста",
      "description": "Визуальное описание...",
      "reference_image_path": "output/locations/1_location_name.jpeg",
      "generation_prompt": "Полный использованный промпт генерации..."
    }
  ],
  "illustrations": [
    {
      "scene_id": 1,
      "story_segment": "Оригинальный текст сцены...",
      "name": "sunny_park_scene",
      "location": {
        "id": 1,
        "name": "Название локации"
      },
      "characters": [
        {
          "id": 1,
          "name": "Имя персонажа",
          "full_body_path": "output/characters/1_character_name.jpeg"
        }
      ],
      "illustration_path": "output/illustrations/1_sunny_park_scene.jpeg",
      "generation_prompt": "Полный использованный промпт генерации..."
    }
  ]
}
```

## 🧪 Разработка и тестирование

В этом проекте для тестирования используется `pytest`. Набор тестов покрывает модели, конфигурацию, управление ассетами, семантику разбиения текста анализатором и обертку ИИ-клиента. Он тщательно тестирует стратегии отката (fallback), замокированные обработчики ввода-вывода PIL, ограничения параллелизма ThreadPool, динамическое сопоставление схем и механизмы повторных попыток с экспоненциальной задержкой.

Для запуска тестов:
```bash
# Сначала активируйте виртуальное окружение
source venv/bin/activate

# Запуск всех тестов с отчетом о покрытии
pytest --cov=app --cov-report=term-missing tests/
```

### Мокирование (Mocking)
В тестах используются `unittest.mock` и `pytest-mock` для имитации ответов API Google GenAI и операций файловой системы, что гарантирует быстрое выполнение тестов без расходования квот API.

## 🏗️ Структура проекта
-   `main.py`: Точка входа и логика оркестрации.
-   `app/`: Основной пакет.
    -   `config.py`: Настройка и управление окружением.
    -   `core/`: Ключевые модули логики.
        -   `ai_client.py`: Обертка для Google GenAI SDK.
        -   `analyzer.py`: Анализ истории (Извлечение Сцен/Персонажей/Локаций).
        -   `asset_manager.py`: Управляет созданием и каталогизацией эталонных ассетов.
        -   `illustrator.py`: Генерирует итоговые иллюстрации сцен.
        -   `models.py`: Модели данных Pydantic.
-   `tests/`: Набор тестов.

## 📜 Лицензия

Этот проект лицензирован под лицензией MIT — подробности см. в файле [LICENSE](LICENSE).