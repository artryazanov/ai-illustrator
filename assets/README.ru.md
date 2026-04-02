> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator — это мощный инструмент, предназначенный для автоматической генерации согласованных высококачественных иллюстраций к историям с использованием моделей Google Gemini как для анализа текста, так и для создания изображений. Он обрабатывает текстовый файл истории, анализирует его для понимания визуального стиля, персонажей и локаций, а затем генерирует последовательность кинематографичных иллюстраций.

## 🖼️ Демонстрация

**Сказка о Колобке**: Для этой демонстрации мы обработали классическую сказку «Колобок». История рассказывает о свежеиспеченном хлебце, который оживает, сбегает от старика со старухой и катится в лес. По пути он поет песенку и перехитряет зайца, волка и медведя, прежде чем, наконец, быть обманутым хитрой лисой.

> **Параметры генерации:**  
> - **Входная история**: Текст сказки «Колобок»  
> - **Подсказка стиля (Style Prompt)**: *"милая и причудливая детская книжная иллюстрация для малышей"*  
> - **Модели**: Текст / Валидатор (`gemini-3.1-pro-preview`), Изображение (`gemini-3.1-flash-image-preview`)
> - **Разрешение и пропорции**: 512px, соотношение сторон `1:1`

### Сгенерированные референсные карточки персонажей

<p align="center">
  <img src="assets/kolobok/characters/2_old_woman.jpeg" width="16%" alt="Old Woman" title="Old Woman" />
  <img src="assets/kolobok/characters/3_little_round_bun.jpeg" width="16%" alt="Little Round Bun" title="Little Round Bun" />
  <img src="assets/kolobok/characters/4_hare.jpeg" width="16%" alt="Hare" title="Hare" />
  <img src="assets/kolobok/characters/5_the_wolf.jpeg" width="16%" alt="The Wolf" title="The Wolf" />
  <img src="assets/kolobok/characters/6_bear.jpeg" width="16%" alt="Bear" title="Bear" />
  <img src="assets/kolobok/characters/7_the_fox.jpeg" width="16%" alt="The Fox" title="The Fox" />
</p>

### Сгенерированные иллюстрации сцен

<p align="center">
  <img src="assets/kolobok/illustrations/1_old_woman_baking_kolobok.jpeg" width="32%" alt="Old Woman Baking" title="Scene 1" />
  <img src="assets/kolobok/illustrations/2_rolling_loaf_escapes.jpeg" width="32%" alt="Rolling Loaf Escapes" title="Scene 2" />
  <img src="assets/kolobok/illustrations/3_kolobok_meets_hare.jpeg" width="32%" alt="Kolobok Meets Hare" title="Scene 3" />
</p>
<p align="center">
  <img src="assets/kolobok/illustrations/4_kolobok_rolls_past_wolf.jpeg" width="32%" alt="Kolobok Rolls Past Wolf" title="Scene 4" />
  <img src="assets/kolobok/illustrations/5_kolobok_escapes_bear.jpeg" width="32%" alt="Kolobok Escapes Bear" title="Scene 5" />
  <img src="assets/kolobok/illustrations/6_fox_eats_kolobok.jpeg" width="32%" alt="Fox Eats Kolobok" title="Scene 6" />
</p>

## ✨ Возможности

-   **Автоматическое определение стиля**: Анализирует текст истории для выбора наиболее подходящего художественного стиля и создает согласованные иллюстрации на его основе.
-   **Согласованность персонажей**:
    -   Извлекает описания персонажей и генерирует их референсные изображения (в полный рост).
    -   Поддерживает постоянный каталог персонажей в `output/data.json`, чтобы один и тот же персонаж выглядел одинаково на протяжении всей истории.
    -   Использует паттерн **Чистых референсов (Clean References)**: Референсные карточки персонажей генерируются строго на изолированном ЧИСТО-БЕЛОМ фоне, чтобы предотвратить смешивание с окружением при интеграции в сцену.
    -   Использует референсные изображения (мультимодальная генерация) для сохранения стабильного внешнего вида персонажей в разных сценах.
-   **Согласованность локаций**:
    -   Генерирует и кэширует референсные изображения локаций (кадры в кинематографичном стиле).
    -   Ведет каталог локаций в `output/data.json` для повторного использования окружения.
    -   **Оптимизация квот**: Умное сопоставление локаций гарантирует, что API генерирует ассеты окружения только для локаций, которые фактически используются в сценах истории, пропуская неиспользуемые фоновые описания.
-   **Генерация кинематографичных сцен**:
    -   Надежно разбивает историю на логические сцены с использованием семантического разделения (сохраняя контекст между фрагментами).
    -   Распараллеливает рендеринг сцен с помощью ThreadPool для ускорения генерации.
    -   Генерирует один целостный кинематографичный кадр для каждой сцены (настраиваемое соотношение сторон).
    -   Применяет **Текстовое якорение (Textual Anchoring)** путем явного сопоставления референсов нескольких персонажей через строго структурированные блоки `MANDATORY VISUAL DETAILS`, что не позволяет модели путать наряды или черты лица разных персонажей.
-   **Цикл QA (LLM-as-a-Judge) и самокоррекция**:
    -   Нативно проверяет сгенерированные изображения на соответствие строгим структурным правилам (например, один кадр, анатомические ограничения, отсутствие текста, отсутствие рамок).
    -   Если изображение не проходит проверку (например, несколько ракурсов, лишние конечности или наличие рамок), строгий валидационный промпт мгновенно запускает блок повторной генерации с ограничениями.
    -   **Интеллектуальный редактор стиля**: Реализует программный контроль качества (AI QA) для проверки текстовых описаний стиля, предотвращая ложноположительные срабатывания (например, путаницу между запрещенным словом "text" и разрешенным словом "texture").
    -   **Сохранение контекста**: Внедренная обратная связь жестко якорит модель для сохранения исходной идентичности персонажа и художественного стиля, исправляя исключительно отмеченную структурную ошибку.
    -   **Обход фильтров безопасности**: Автоматически очищает сырые ошибки QA с помощью промежуточного LLM-прохода «Промпт-инженера». Это переводит негативный фидбек (например, "удалить водяной знак/подпись") в позитивные, визуально понятные промпты, которые безопасно обходят блокировки фильтров генератора изображений.
    -   Применяет QA-валидацию единообразно к **Шаблонам стиля**, **Персонажам**, **Локациям** и **Сценам** для поддержания целостного повествования без артефактов.
-   **Нативные структурированные выводы (Structured Outputs)**:
    -   Заменяет хрупкий парсинг markdown-JSON на 100% надежную поддержку `response_schema` Google GenAI, напрямую связанную с моделями Pydantic.
-   **Отказоустойчивость API**:
    -   Полностью обрабатывает лимиты запросов к API, тайм-ауты и сбои данных, используя механизмы повторных попыток с экспоненциальной задержкой (`tenacity`).
-   **Поддержка Docker**: Полностью контейнеризировано для простоты развертывания и запуска.
-   **Комплексное тестирование**: Высокое покрытие тестами при непрерывной интеграции через Github Actions и Codecov.

## 🛠️ Предварительные требования

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
Скопируйте пример файла окружения и добавьте свой API-ключ.
```bash
cp .env.example .env
```
Откройте файл `.env` и настройте переменные:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # или совместимая
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # или конкретная модель imagen
IMAGE_RESOLUTION=1K # Варианты: 512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # Варианты: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # Максимальное количество попыток генерации в циклах QA
```

### 3. Запуск через Docker (Рекомендуется)

Соберите Docker-образ:
```bash
docker-compose build
```

Запустите генератор:
1.  Поместите текстовый файл с вашей историей в директорию `data/` (например, `data/my_story.txt`).
2.  Выполните запуск контейнера:
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *Примечание: директория `output` с результатами работы будет заполнена на вашей хост-машине.*

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
-   `--text-file`: **(Обязательно)** Путь к входному текстовому файлу с историей.
-   `--output-dir`: Директория для сохранения сгенерированных ассетов и иллюстраций (по умолчанию: `output`).
-   `--style-prompt`: Необязательный промпт для направления изначального определения стиля (например, "Киберпанк аниме", "Картина маслом").

### Структура вывода
Инструмент создает организованную и плоскую структуру директории вывода:

```
output/
├── characters/             # Ассеты персонажей
│   └── 1_character_name.jpeg
├── locations/              # Ассеты локаций
│   └── 1_location_name.jpeg
├── illustrations/          # Финальные иллюстрации сцен
│   └── 1_sunny_park_scene.jpeg
├── data.json               # Единый манифест (Стиль, Персонажи, Локации, Иллюстрации)
└── style_templates/        # Сгенерированные базовые изображения стиля
    ├── style_reference_fullbody.jpg   # Динамический референс стиля для персонажей
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
      "generation_prompt": "Полный промпт, использованный для генерации..."
    }
  ],
  "locations": [
    {
      "id": 1,
      "name": "Имя локации",
      "original_name": "Оригинальное имя из текста",
      "description": "Визуальное описание...",
      "reference_image_path": "output/locations/1_location_name.jpeg",
      "generation_prompt": "Полный промпт, использованный для генерации..."
    }
  ],
  "illustrations": [
    {
      "scene_id": 1,
      "story_segment": "Оригинальный текст сцены...",
      "name": "sunny_park_scene",
      "location": {
        "id": 1,
        "name": "Имя локации"
      },
      "characters": [
        {
          "id": 1,
          "name": "Имя персонажа",
          "full_body_path": "output/characters/1_character_name.jpeg"
        }
      ],
      "illustration_path": "output/illustrations/1_sunny_park_scene.jpeg",
      "generation_prompt": "Полный промпт, использованный для генерации..."
    }
  ]
}
```

## 🧪 Разработка и тестирование

В этом проекте для тестирования используется `pytest`. Набор тестов покрывает модели, конфигурацию, управление ассетами, семантику разбиения текста в анализаторе и обертку ИИ-клиента. Он тщательно тестирует резервные стратегии, замоканные (mock) обработчики ввода-вывода PIL, лимиты параллелизма ThreadPool, динамическое сопоставление схем и механизмы повторных попыток с экспоненциальной задержкой.

Для запуска тестов:
```bash
# Сначала активируйте виртуальное окружение
source venv/bin/activate

# Запустите все тесты с отчетом о покрытии
pytest --cov=app --cov-report=term-missing tests/
```

### Мокирование (Mocking)
Тесты используют `unittest.mock` и `pytest-mock` для имитации ответов API Google GenAI и операций с файловой системой, гарантируя, что тесты выполняются быстро и не расходуют квоту API.

## 🏗️ Структура проекта
-   `main.py`: Точка входа и логика оркестрации.
-   `app/`: Основной пакет.
    -   `config.py`: Управление конфигурацией и переменными окружения.
    -   `core/`: Ключевые модули логики.
        -   `ai_client.py`: Обертка для Google GenAI SDK.
        -   `analyzer.py`: Анализ истории (извлечение сцен, персонажей, локаций).
        -   `asset_manager.py`: Управление созданием и каталогизацией референсных ассетов.
        -   `illustrator.py`: Генерация финальных иллюстраций к сценам.
        -   `models.py`: Модели данных Pydantic.
-   `tests/`: Набор тестов.

## 📜 Лицензия

Этот проект лицензирован по лицензии MIT — подробности см. в файле [LICENSE](LICENSE).