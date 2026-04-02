> 🌐 **اللغات:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

يعد AI Illustrator أداة قوية مصممة لتوليد رسومات توضيحية متسقة وعالية الجودة للقصص تلقائيًا باستخدام نماذج Gemini من Google لكل من تحليل النصوص وتوليد الصور. يقوم بمعالجة ملف نصي للقصة، ويحلله لفهم النمط البصري والشخصيات والمواقع، ثم يولد سلسلة من الرسومات التوضيحية السينمائية.

## 🖼️ معرض الأعمال

**حكاية كولوبوك (The Tale of Kolobok)**: في هذا العرض التوضيحي، قمنا بمعالجة الحكاية الخرافية الكلاسيكية "كولوبوك" (الكعكة المستديرة الصغيرة). تدور القصة حول كعكة مخبوزة حديثًا تدب فيها الحياة، وتهرب من رجل وامرأة عجوزين، وتتدحرج بعيدًا في الغابة. خلال رحلتها، تغني أغنية وتتفوق بذكائها على أرنب وذئب ودب، قبل أن يتغلب عليها ثعلب ماكر في النهاية.

> **معلمات التوليد:**  
> - **المدخلات القصصية**: نص حكاية كولوبوك  
> - **مُلقّن النمط (Style Prompt)**: *"cute and whimsical children's book illustration for toddlers" (رسومات كتب أطفال لطيفة وغريبة الأطوار للأطفال الصغار)*  
> - **النماذج المستخدمة**: النص / المدقق (`gemini-3.1-pro-preview`)، الصورة (`gemini-3.1-flash-image-preview`)
> - **سياق الدقة**: 512 بكسل، نسبة العرض إلى الارتفاع `1:1`

### بطاقات مرجعية للشخصيات المُولّدة

<p align="center">
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/2_old_woman.jpeg" width="16%" alt="Old Woman" title="Old Woman" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/3_little_round_bun.jpeg" width="16%" alt="Little Round Bun" title="Little Round Bun" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/4_hare.jpeg" width="16%" alt="Hare" title="Hare" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/5_the_wolf.jpeg" width="16%" alt="The Wolf" title="The Wolf" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/6_bear.jpeg" width="16%" alt="Bear" title="Bear" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/7_the_fox.jpeg" width="16%" alt="The Fox" title="The Fox" />
</p>

### رسومات المشاهد المُولّدة

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

-   **اكتشاف النمط تلقائيًا**: يحلل نص القصة لتحديد النمط الفني الأنسب ويولد رسومات توضيحية متسقة بناءً على هذا النمط.
-   **اتساق الشخصيات**:
    -   يستخرج أوصاف الشخصيات ويولد صورًا مرجعية لها (الجسم بالكامل).
    -   يحتفظ بكتالوج دائم للشخصيات في `output/data.json` لضمان ظهور نفس الشخصية بشكل متسق طوال القصة.
    -   يستخدم نمط **المراجع النظيفة (Clean References)**: يتم إنشاء البطاقات المرجعية للشخصيات بدقة على خلفيات بيضاء نقية معزولة لمنع تداخل البيئة المحيطة أثناء دمج المشاهد.
    -   يستخدم الصور المرجعية (التوليد متعدد الوسائط) للحفاظ على استقرار مظهر الشخصية عبر المشاهد المختلفة.
-   **اتساق المواقع**:
    -   يولد ويخزن صورًا مرجعية للمواقع (لقطات بأسلوب سينمائي).
    -   يحتفظ بكتالوج للمواقع في `output/data.json` لإعادة استخدام الإعدادات.
    -   **تحسين الحصص (Quota Optimization)**: تضمن مطابقة المواقع الذكية أن واجهة برمجة التطبيقات (API) تولد فقط أصول البيئة للمواقع النشطة فعليًا في مشاهد القصة، متجاوزة أوصاف الخلفيات غير المستخدمة.
-   **توليد المشاهد السينمائية**:
    -   يقسم القصة إلى مشاهد منطقية بشكل آمن باستخدام التقسيم الدلالي (مع الحفاظ على السياق عبر الأجزاء).
    -   يوازي عملية تصيير المشاهد عبر `ThreadPool` لتوليد أسرع.
    -   يولد إطارًا سينمائيًا واحدًا متماسكًا لكل مشهد (نسبة العرض إلى الارتفاع قابلة للتكوين).
    -   يستخدم **الارتساء النصي (Textual Anchoring)** من خلال تعيين مراجع متعددة للشخصيات بشكل صريح عبر كتل `MANDATORY VISUAL DETAILS` منظمة بدقة لمنع النموذج من الخلط بين الأزياء أو الملامح بين الشخصيات.
-   **حلقة ضمان الجودة (QA) باستخدام النموذج اللغوي كحكم (LLM-as-a-Judge) والتصحيح الذاتي**:
    -   يتحقق محليًا من الصور المُولّدة مقابل مجموعات قواعد هيكلية صارمة (مثل: إطار واحد، قيود التشريح، عدم وجود نص، عدم وجود حدود).
    -   إذا فشلت صورة ما (على سبيل المثال، زوايا متعددة، أطراف إضافية، أو حدود إطارية)، يقوم مُلقّن تحقق صارم بتشغيل كتلة إعادة توليد مقيدة على الفور.
    -   **محرر النمط الذكي**: ينفذ ضمان الجودة المبرمج بالذكاء الاصطناعي للتحقق من أوصاف الأنماط النصية، مما يمنع الإبلاغات الإيجابية الكاذبة (مثل الخلط بين الكلمة المحظورة "text" داخل الكلمة المسموحة "texture").
    -   **الحفاظ على السياق**: تعمل الملاحظات المحقونة على تثبيت النموذج بقوة للاحتفاظ بالهوية الأصلية للشخصية والنمط الفني مع إصلاح الخطأ الهيكلي المُلاحظ حصريًا.
    -   **تجاوز فلتر الأمان**: يقوم بتعقيم إخفاقات ضمان الجودة الخام تلقائيًا من خلال تمرير وسيط للنموذج اللغوي الكبير بصفته "مهندس أوامر". يترجم هذا الملاحظات السلبية (مثل "إزالة العلامة المائية/التوقيع") إلى أوامر إيجابية واضحة بصريًا تتجاوز فلاتر الحظر الخاصة بمولد الصور بأمان.
    -   يطبق التحقق من ضمان الجودة بشكل موحد عبر **قوالب الأنماط**، **الشخصيات**، **المواقع**، و**المشاهد** للحفاظ على سرد متماسك وخالٍ من العيوب.
-   **مخرجات هيكلية أصلية**:
    -   يستبدل تحليل markdown-JSON الهش بدعم `response_schema` الموثوق بنسبة 100% من Google GenAI والمُعيّن مباشرة إلى نماذج Pydantic.
-   **مرونة واجهة برمجة التطبيقات (API)**:
    -   يتعامل بشكل كامل مع حدود معدل واجهة برمجة التطبيقات، ومهلات الاتصال، وفشل الحمولات باستخدام آليات إعادة المحاولة ذات التراجع الأسي (`tenacity`).
-   **دعم Docker**: مُعبأ بالكامل في حاويات لسهولة النشر والتنفيذ.
-   **اختبار شامل**: تغطية اختبارية عالية تحت التكامل المستمر باستخدام Github Actions و Codecov.

## 🛠️ المتطلبات الأساسية

-   **Python 3.12+** (إذا كان التشغيل محليًا)
-   **Docker** و **Docker Compose** (يُنصح بهما للعزل)
-   **مفتاح واجهة برمجة تطبيقات Google Cloud (API Key)** مع صلاحية الوصول إلى نماذج Gemini (بما في ذلك قدرات توليد الصور).

## 🚀 التثبيت والإعداد

### 1. استنساخ المستودع
```bash
git clone git@github.com:artryazanov/ai-illustrator.git
cd ai-illustrator
```

### 2. تكوين البيئة
انسخ ملف البيئة التجريبي وأضف مفتاح API الخاص بك.
```bash
cp .env.example .env
```
افتح ملف `.env` وقم بتعيين المتغيرات الخاصة بك:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # or compatible
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # or specific imagen model
IMAGE_RESOLUTION=1K # Options: 512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # Options: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # Maximum generation attempts during QA loops
```

### 3. التشغيل باستخدام Docker (مُستحسن)

بناء صورة Docker:
```bash
docker-compose build
```

تشغيل المُولّد:
1.  ضع ملف النص الخاص بقصتك في مجلد `data/` (على سبيل المثال، `data/my_story.txt`).
2.  قم بتنفيذ الحاوية:
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
-   `--text-file`: **(مطلوب)** مسار ملف النص المُدخل الذي يحتوي على القصة.
-   `--output-dir`: المجلد المخصص لحفظ الأصول والرسومات التوضيحية المُولّدة (الافتراضي: `output`).
-   `--style-prompt`: مُلقّن اختياري لتوجيه عملية اكتشاف النمط الأولي (مثل: "Cyberpunk anime"، "Oil painting").

### هيكل المخرجات
تقوم الأداة بإنشاء مجلد مخرجات مسطح ومنظم:

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

### هيكل `data.json`
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

يستخدم هذا المشروع `pytest` للاختبار. تغطي مجموعة الاختبار النماذج، والتكوين، وإدارة الأصول، ودلالات تقسيم نص المحلل، وغلاف عميل الذكاء الاصطناعي. كما تختبر بشكل صارم استراتيجيات التراجع (Fallback)، ومعالجات الإدخال والإخراج الوهمية لـ PIL، وحدود التزامن في ThreadPool، وتعيينات المخطط الديناميكية، وآليات إعادة المحاولة ذات التراجع الأسي.

لتشغيل الاختبارات:
```bash
# Activate your virtual environment first
source venv/bin/activate

# Run all tests with coverage reporting
pytest --cov=app --cov-report=term-missing tests/
```

### المحاكاة (Mocking)
تستخدم الاختبارات `unittest.mock` و `pytest-mock` لمحاكاة استجابات واجهة برمجة تطبيقات Google GenAI وعمليات نظام الملفات، مما يضمن أن تكون الاختبارات سريعة ولا تستهلك حصة واجهة برمجة التطبيقات (API Quota).

## 🏗️ هيكل المشروع
-   `main.py`: نقطة الدخول ومنطق التنسيق.
-   `app/`: الحزمة الأساسية.
    -   `config.py`: إدارة التكوين والبيئة.
    -   `core/`: وحدات المنطق الرئيسية.
        -   `ai_client.py`: غلاف لحزمة تطوير برمجيات Google GenAI.
        -   `analyzer.py`: تحليل القصة (استخراج المشاهد/الشخصيات/المواقع).
        -   `asset_manager.py`: يدير إنشاء وفهرسة الأصول المرجعية.
        -   `illustrator.py`: يولد رسومات المشاهد النهائية.
        -   `models.py`: نماذج بيانات Pydantic.
-   `tests/`: مجموعة الاختبارات.

## 📜 الترخيص

هذا المشروع مرخص بموجب ترخيص MIT - راجع ملف [LICENSE](LICENSE) للحصول على التفاصيل.