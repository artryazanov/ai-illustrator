> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator هي أداة قوية مصممة لإنشاء رسومات توضيحية متسقة وعالية الجودة للقصص تلقائيًا باستخدام نماذج Gemini من Google لتحليل النص وإنشاء الصور على حد سواء. تقوم الأداة بمعالجة ملف نصي للقصة، وتحليله لفهم النمط البصري، الشخصيات، والمواقع، ثم تقوم بإنشاء سلسلة من الرسومات التوضيحية السينمائية.

## 🖼️ معرض الأعمال

**حكاية كولوبوك**: في هذا العرض التوضيحي، قمنا بمعالجة القصة الخيالية الكلاسيكية "كولوبوك" (الكعكة الدائرية الصغيرة). تدور القصة حول كعكة مخبوزة حديثًا تدب فيها الحياة، وتهرب من رجل عجوز وامرأة عجوز، وتتدحرج بعيدًا في الغابة. خلال رحلتها، تغني أغنية وتتغلب بذكائها على أرنب بري، وذئب، ودب، قبل أن يتغلب عليها في النهاية ثعلب ماكر.

> **معلمات الإنشاء:**  
> - **القصة المدخلة**: نص كولوبوك  
> - **موجه النمط**: *"رسومات توضيحية لكتب أطفال لطيفة وغريبة الأطوار للأطفال الصغار"*  
> - **النماذج**: النص / المدقق (`gemini-3.1-pro-preview`)، الصورة (`gemini-3.1-flash-image-preview`)
> - **سياق الدقة**: 512 بكسل، نسبة العرض إلى الارتفاع `1:1`

### بطاقات مرجعية للشخصيات المُنشأة

<p align="center">
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/2_old_woman.jpeg" width="16%" alt="Old Woman" title="Old Woman" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/3_little_round_bun.jpeg" width="16%" alt="Little Round Bun" title="Little Round Bun" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/4_hare.jpeg" width="16%" alt="Hare" title="Hare" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/5_the_wolf.jpeg" width="16%" alt="The Wolf" title="The Wolf" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/6_bear.jpeg" width="16%" alt="Bear" title="Bear" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/7_the_fox.jpeg" width="16%" alt="The Fox" title="The Fox" />
</p>

### رسومات مشاهد القصة المُنشأة

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

## ✨ الميزات

-   **اكتشاف النمط التلقائي**: يحلل نص القصة لتحديد النمط الفني الأنسب ويقوم بإنشاء رسومات توضيحية متسقة بناءً على هذا النمط.
-   **اتساق الشخصيات**:
    -   يستخرج أوصاف الشخصيات ويقوم بإنشاء صور مرجعية للشخصيات (بكامل الجسم).
    -   يحتفظ بكتالوج دائم للشخصيات في `output/data.json` لضمان ظهور نفس الشخصية بشكل متسق طوال القصة.
    -   يستخدم نمط **المراجع النظيفة (Clean References)**: يتم إنشاء البطاقات المرجعية للشخصيات بصرامة على خلفيات بيضاء نقية معزولة لمنع تداخل البيئة المحيطة أثناء دمج المشاهد.
    -   يستخدم الصور المرجعية (التوليد متعدد الوسائط) للحفاظ على استقرار مظهر الشخصية عبر المشاهد المختلفة.
-   **اتساق المواقع**:
    -   يقوم بإنشاء وتخزين صور مرجعية للمواقع (لقطات بأسلوب سينمائي).
    -   يحتفظ بكتالوج للمواقع في `output/data.json` لإعادة استخدام الإعدادات.
    -   **تحسين استهلاك الحصة (Quota Optimization)**: تضمن المطابقة الذكية للمواقع أن تقوم واجهة برمجة التطبيقات (API) بإنشاء أصول بيئية فقط للمواقع النشطة فعليًا في مشاهد القصة، متجاهلة أوصاف الخلفيات غير المستخدمة.
-   **إنشاء مشاهد سينمائية**:
    -   يقسم القصة إلى مشاهد منطقية بشكل آمن باستخدام التقسيم الدلالي (مع الحفاظ على السياق عبر الأجزاء المقطعة).
    -   يوازي عملية تصيير المشاهد عبر ThreadPool للحصول على إنشاء أسرع.
    -   يُنشئ إطاراً سينمائياً واحداً متماسكاً لكل مشهد (مع إمكانية تخصيص نسبة العرض إلى الارتفاع).
    -   يستخدم **الارتساء النصي (Textual Anchoring)** عن طريق ربط مراجع الشخصيات المتعددة صراحةً عبر كتل `MANDATORY VISUAL DETAILS` منظمة بدقة لمنع النموذج من الخلط بين الأزياء أو الميزات بين الشخصيات.
-   **حلقة ضمان الجودة باستخدام النموذج اللغوي كحكم (LLM-as-a-Judge) والتصحيح الذاتي**:
    -   يتحقق تلقائيًا من صحة الصور المُنشأة مقابل مجموعات قواعد هيكلية صارمة (مثل: إطار واحد، قيود التشريح، بدون نص، بدون حدود).
    -   إذا فشلت الصورة (على سبيل المثال، زوايا متعددة، أطراف زائدة، أو حدود تأطير)، فإن موجه تحقق صارم يطلق فوراً كتلة إعادة إنشاء مقيدة.
    -   **محرر النمط الذكي**: يطبق ضمان جودة برمجي بالذكاء الاصطناعي للتحقق من أوصاف نمط النص، مما يمنع العلامات الإيجابية الخاطئة (مثل الخلط بين الكلمة المحظورة "text" داخل الكلمة المسموحة "texture").
    -   **الحفاظ على السياق**: تعمل الملاحظات المحقونة على تثبيت النموذج بقوة للاحتفاظ بهوية الشخصية الأصلية والنمط الفني مع إصلاح الخطأ الهيكلي المُلاحظ حصريًا.
    -   **تجاوز فلتر الأمان**: يقوم بتطهير إخفاقات ضمان الجودة الخام تلقائيًا من خلال تمريرة وسيطة لنموذج لغوي "مهندس موجهات". هذا يترجم الملاحظات السلبية (مثل "إزالة العلامة المائية/التوقيع") إلى موجهات إيجابية وواضحة بصريًا تتجاوز بأمان فلاتر حظر منشئ الصور.
    -   يطبق التحقق من ضمان الجودة بشكل موحد عبر **قوالب النمط**، و**الشخصيات**، و**المواقع**، و**المشاهد** للحفاظ على سرد متماسك وخالٍ من العيوب.
-   **المخرجات المهيكلة الأصلية**:
    -   يستبدل تحليل markdown-JSON الهش بدعم `response_schema` موثوق بنسبة 100% من Google GenAI، والذي يتم تعيينه مباشرة إلى نماذج Pydantic.
-   **مرونة واجهة برمجة التطبيقات (API)**:
    -   يتعامل بالكامل مع حدود معدل واجهة برمجة التطبيقات، ومهلات الاتصال، وفشل الحمولات باستخدام آليات إعادة المحاولة التراجعية الأسية (`tenacity`).
-   **دعم Docker**: معبأ في حاويات بالكامل لسهولة النشر والتنفيذ.
-   **اختبار شامل**: تغطية اختبار عالية في ظل التكامل المستمر باستخدام Github Actions و Codecov.

## 🛠️ المتطلبات الأساسية

-   **Python 3.12+** (في حالة التشغيل محليًا)
-   **Docker** و **Docker Compose** (موصى بهما للعزل)
-   **مفتاح واجهة برمجة تطبيقات Google Cloud** مع إمكانية الوصول إلى نماذج Gemini (بما في ذلك إمكانات إنشاء الصور).

## 🚀 التثبيت والإعداد

### 1. استنساخ المستودع
```bash
git clone git@github.com:artryazanov/ai-illustrator.git
cd ai-illustrator
```

### 2. تكوين البيئة
انسخ ملف البيئة كمثال وأضف مفتاح API الخاص بك.
```bash
cp .env.example .env
```
افتح ملف `.env` وقم بتعيين المتغيرات الخاصة بك:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # or compatible
VALIDATOR_MODEL_NAME=gemini-3.1-pro-preview # or compatible
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # or specific imagen model
IMAGE_RESOLUTION=1K # Options: 512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # Options: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # Maximum generation attempts during QA loops
```

### 3. التشغيل باستخدام Docker (موصى به)

بناء صورة Docker:
```bash
docker-compose build
```

تشغيل المولد:
1. ضع ملف نص القصة الخاص بك في مجلد `data/` (على سبيل المثال، `data/my_story.txt`).
2. نفّذ الحاوية:
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *ملاحظة: سيتم ملء مجلد `output` بالنتائج على جهازك المضيف.*

### 4. التشغيل محليًا

إنشاء بيئة افتراضية:
```bash
python3 -m venv venv
source venv/bin/activate
```

تثبيت التبعيات:
```bash
pip install -r requirements.txt
```

تشغيل التطبيق:
```bash
python main.py --text-file data/my_story.txt --output-dir output/my_project_name
```

## 💡 الاستخدام

### وسائط سطر الأوامر
-   `--text-file`: **(مطلوب)** مسار ملف النص المدخل الذي يحتوي على القصة.
-   `--output-dir`: المجلد المخصص لحفظ الأصول والرسومات التوضيحية المُنشأة (الافتراضي: `output`).
-   `--style-prompt`: موجه اختياري لتوجيه عملية اكتشاف النمط الأولي (مثل: "Cyberpunk anime"، "Oil painting").

### هيكل المخرجات
تُنشئ الأداة مجلد مخرجات مسطح ومنظم:

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

### هيكل ملف `data.json`
يعمل ملف `data.json` كبيان مركزي (Manifest) للمشروع.

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

## 🧪 التطوير والاختبار

يستخدم هذا المشروع `pytest` للاختبار. تغطي مجموعة الاختبار النماذج، والتكوين، وإدارة الأصول، ودلالات تقسيم النص في المحلل، وغلاف عميل الذكاء الاصطناعي. كما تختبر بدقة استراتيجيات التراجع، ومعالجات إدخال/إخراج PIL الوهمية (Mocked)، وحدود التزامن في ThreadPool، وتعيينات المخطط الديناميكية، وآليات إعادة المحاولة التراجعية الأسية.

لتشغيل الاختبارات:
```bash
# Activate your virtual environment first
source venv/bin/activate

# Run all tests with coverage reporting
pytest --cov=app --cov-report=term-missing tests/
```

### المحاكاة (Mocking)
تستخدم الاختبارات `unittest.mock` و `pytest-mock` لمحاكاة استجابات واجهة برمجة تطبيقات Google GenAI وعمليات نظام الملفات، مما يضمن سرعة الاختبارات وعدم استهلاك حصة واجهة برمجة التطبيقات.

## 🏗️ هيكل المشروع
-   `main.py`: نقطة الدخول ومنطق التنسيق.
-   `app/`: الحزمة الأساسية.
    -   `config.py`: إدارة التكوين والبيئة.
    -   `core/`: وحدات المنطق الرئيسية.
        -   `ai_client.py`: غلاف لحزمة تطوير برمجيات (SDK) الخاصة بـ Google GenAI.
        -   `analyzer.py`: تحليل القصة (استخراج المشهد/الشخصية/الموقع).
        -   `asset_manager.py`: يدير إنشاء وفهرسة الأصول المرجعية.
        -   `illustrator.py`: يقوم بإنشاء رسومات المشاهد النهائية.
        -   `models.py`: نماذج بيانات Pydantic.
-   `tests/`: مجموعة الاختبارات.

## 📜 الترخيص

هذا المشروع مرخص بموجب ترخيص MIT - راجع ملف [الترخيص (LICENSE)](LICENSE) للحصول على التفاصيل.