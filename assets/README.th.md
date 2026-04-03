> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator เป็นเครื่องมืออันทรงพลังที่ออกแบบมาเพื่อสร้างภาพประกอบสำหรับนิทานหรือเรื่องราวอย่างสม่ำเสมอและมีคุณภาพสูงโดยอัตโนมัติ โดยใช้โมเดล Gemini ของ Google สำหรับทั้งการวิเคราะห์ข้อความและการสร้างภาพประกอบ เครื่องมือนี้จะประมวลผลไฟล์ข้อความเรื่องราว วิเคราะห์เพื่อทำความเข้าใจสไตล์ภาพ ตัวละคร และสถานที่ จากนั้นจึงสร้างลำดับของภาพประกอบในรูปแบบภาพยนตร์ (cinematic illustrations)

## 🖼️ ผลงานตัวอย่าง

**นิทานเรื่อง Kolobok**: สำหรับการสาธิตนี้ เราได้นำนิทานคลาสสิกเรื่อง "Kolobok" (ก้อนขนมปังกลม) มาประมวลผล เรื่องราวเกี่ยวกับก้อนขนมปังอบใหม่ๆ ที่มีชีวิตขึ้นมา หลบหนีจากชายชราและหญิงชรา และกลิ้งเข้าไปในป่า ระหว่างการเดินทาง มันได้ร้องเพลงและเอาชนะกระต่าย หมาป่า และหมี ด้วยสติปัญญา ก่อนที่จะถูกสุนัขจิ้งจอกเจ้าเล่ห์หลอกล่อในท้ายที่สุด

> **พารามิเตอร์การสร้าง:**  
> - **ข้อมูลเรื่องราวต้นทาง (Story Input)**: ข้อความเรื่อง Kolobok
> - **พรอมต์กำหนดสไตล์ (Style Prompt)**: *"cute and whimsical children's book illustration for toddlers"*  
> - **โมเดล (Models)**: ข้อความ / การตรวจสอบ (`gemini-3.1-pro-preview`), รูปภาพ (`gemini-3.1-flash-image-preview`)
> - **ความละเอียด (Resolution Context)**: 512px, อัตราส่วนภาพ `1:1`

### การ์ดข้อมูลอ้างอิงตัวละครที่สร้างขึ้น

<p align="center">
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/2_old_woman.jpeg" width="16%" alt="Old Woman" title="Old Woman" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/3_little_round_bun.jpeg" width="16%" alt="Little Round Bun" title="Little Round Bun" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/4_hare.jpeg" width="16%" alt="Hare" title="Hare" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/5_the_wolf.jpeg" width="16%" alt="The Wolf" title="The Wolf" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/6_bear.jpeg" width="16%" alt="Bear" title="Bear" />
  <img src="https://raw.githubusercontent.com/artryazanov/ai-illustrator/main/assets/kolobok/characters/7_the_fox.jpeg" width="16%" alt="The Fox" title="The Fox" />
</p>

### ภาพประกอบฉากที่สร้างขึ้น

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

## ✨ คุณสมบัติหลัก

-   **ตรวจจับสไตล์โดยอัตโนมัติ**: วิเคราะห์ข้อความในเรื่องราวเพื่อกำหนดสไตล์ศิลปะที่เหมาะสมที่สุด และสร้างภาพประกอบที่มีความสม่ำเสมอตามสไตล์นั้น
-   **ความสม่ำเสมอของตัวละคร**:
    -   ดึงคำอธิบายตัวละครและสร้างรูปภาพตัวละครอ้างอิง (แบบเต็มตัว)
    -   เก็บข้อมูลและรักษารายการแคตตาล็อกตัวละครใน `output/data.json` เพื่อให้แน่ใจว่าตัวละครตัวเดิมจะมีหน้าตาที่สม่ำเสมอตลอดทั้งเรื่อง
    -   ใช้รูปแบบ **Clean References**: การ์ดอ้างอิงตัวละครจะถูกสร้างขึ้นบนพื้นหลังสีขาวล้วนอย่างเคร่งครัด เพื่อป้องกันไม่ให้สีของสภาพแวดล้อมปะปนเข้ามาเมื่อนำไปรวมในฉาก
    -   ใช้รูปภาพอ้างอิง (การสร้างแบบ multimodal) เพื่อรักษาหน้าตาของตัวละครให้คงที่ในฉากต่างๆ
-   **ความสม่ำเสมอของสถานที่**:
    -   สร้างและแคชรูปภาพสถานที่อ้างอิง (ภาพสไตล์ภาพยนตร์)
    -   เก็บรายการแคตตาล็อกสถานที่ใน `output/data.json` เพื่อนำการตั้งค่ากลับมาใช้ใหม่
    -   **การเพิ่มประสิทธิภาพโควตา (Quota Optimization)**: การจับคู่สถานที่แบบชาญฉลาดช่วยให้แน่ใจว่า API จะสร้างทรัพย์สินด้านสภาพแวดล้อมเฉพาะสำหรับสถานที่ที่ใช้งานจริงในฉากของเรื่องราวเท่านั้น โดยข้ามคำอธิบายพื้นหลังที่ไม่ได้ใช้งาน
-   **การสร้างฉากในรูปแบบภาพยนตร์**:
    -   แบ่งเรื่องราวออกเป็นฉากตามตรรกะอย่างปลอดภัยโดยใช้ Semantic Chunking (การรักษาบริบทข้ามส่วนต่างๆ)
    -   สร้างการเรนเดอร์ฉากแบบคู่ขนาน (Parallelizes) ผ่าน ThreadPool เพื่อการสร้างภาพที่เร็วขึ้น
    -   สร้างเฟรมภาพยนตร์ที่สอดคล้องเป็นหนึ่งเดียวสำหรับแต่ละฉาก (กำหนดอัตราส่วนภาพได้)
    -   ใช้ **Textual Anchoring** โดยการจับคู่การอ้างอิงตัวละครหลายตัวอย่างชัดเจนผ่านบล็อก `MANDATORY VISUAL DETAILS` ที่มีโครงสร้างอย่างเคร่งครัด เพื่อป้องกันไม่ให้โมเดลสับสนระหว่างชุดหรือลักษณะของตัวละคร
-   **ลูปการตรวจสอบคุณภาพด้วย LLM-as-a-Judge และการแก้ไขตัวเอง**:
    -   ตรวจสอบรูปภาพที่สร้างขึ้นตามชุดกฎโครงสร้างที่เข้มงวดโดยกำเนิด (เช่น เฟรมเดี่ยว ข้อจำกัดทางกายวิภาค ไม่มีข้อความ ไม่มีขอบ)
    -   หากรูปภาพไม่ผ่านเกณฑ์ (เช่น มีหลายมุมมอง มีแขนขาเกิน หรือมีกรอบรูป) พรอมต์การตรวจสอบที่เข้มงวดจะสั่งงานบล็อกให้สร้างรูปภาพใหม่ภายใต้ข้อจำกัดทันที
    -   **เครื่องมือแก้ไขสไตล์อัจฉริยะ (Intelligent Style Editor)**: นำ AI QA เชิงโปรแกรมมาใช้เพื่อตรวจสอบคำอธิบายสไตล์ที่เป็นข้อความ ป้องกันการแจ้งเตือนผิดพลาด (false-positive) (เช่น การสับสนระหว่างคำที่ถูกแบน "text" กับคำที่อนุญาต "texture")
    -   **การรักษาบริบท (Context Preservation)**: ความคิดเห็นที่ส่งกลับไปจะช่วยยึดโยงให้โมเดลรักษาเอกลักษณ์ของตัวละครเดิมและสไตล์ศิลปะไว้ได้อย่างเหนียวแน่น ในขณะที่เน้นแก้ไขเฉพาะข้อผิดพลาดทางโครงสร้างที่ตรวจพบเท่านั้น
    -   **การข้ามตัวกรองความปลอดภัย (Safety Filter Bypass)**: ทำความสะอาดข้อผิดพลาด QA ดิบโดยอัตโนมัติผ่านตัวกลาง LLM "Prompt Engineer" ซึ่งจะแปลงความคิดเห็นเชิงลบ (เช่น "ลบลายน้ำ/ลายเซ็น") เป็นพรอมต์เชิงบวกและมองเห็นได้ชัดเจนที่สามารถข้ามตัวกรองบล็อกการสร้างรูปภาพได้อย่างปลอดภัย
    -   นำการตรวจสอบคุณภาพ (QA validation) มาใช้อย่างสม่ำเสมอกับ **เทมเพลตสไตล์**, **ตัวละคร**, **สถานที่**, และ **ฉาก** เพื่อรักษาการเล่าเรื่องที่กลมกลืนและปราศจากข้อบกพร่องของภาพ
-   **เอาต์พุตที่มีโครงสร้างโดยกำเนิด (Native Structured Outputs)**:
    -   แทนที่การแยกส่วน markdown-JSON ที่เปราะบางด้วยการรองรับ `response_schema` ของ Google GenAI ที่เชื่อถือได้ 100% ซึ่งแมปกับโมเดล Pydantic โดยตรง
-   **ความยืดหยุ่นของ API (API Resilience)**:
    -   จัดการกับข้อจำกัดอัตราการเรียกใช้งาน API (rate limits), หมดเวลา (timeouts) และความล้มเหลวของเพย์โหลดได้อย่างเต็มรูปแบบโดยใช้กลไกการลองใหม่แบบ exponential backoff (`tenacity`)
-   **รองรับ Docker**: ทำงานแบบคอนเทนเนอร์เต็มรูปแบบเพื่อให้ง่ายต่อการปรับใช้และการรันระบบ
-   **การทดสอบที่ครอบคลุม**: ครอบคลุมการทดสอบในระดับสูงภายใต้การรวมอย่างต่อเนื่อง (CI) ด้วย Github Actions และ Codecov

## 🛠️ ข้อกำหนดเบื้องต้น

-   **Python 3.12+** (หากรันในเครื่องของคุณเอง)
-   **Docker** และ **Docker Compose** (แนะนำสำหรับการรันแบบแยกส่วน)
-   **Google Cloud API Key** ที่มีสิทธิ์เข้าถึงโมเดล Gemini (รวมถึงความสามารถในการสร้างรูปภาพ)

## 🚀 การติดตั้งและการตั้งค่า

### 1. โคลน Repository
```bash
git clone git@github.com:artryazanov/ai-illustrator.git
cd ai-illustrator
```

### 2. กำหนดค่าสภาพแวดล้อม (Environment)
คัดลอกไฟล์ตัวอย่าง environment และเพิ่ม API key ของคุณ
```bash
cp .env.example .env
```
เปิดไฟล์ `.env` และตั้งค่าตัวแปรของคุณ:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # or compatible
VALIDATOR_MODEL_NAME=gemini-3.1-pro-preview # or compatible
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # or specific imagen model
IMAGE_RESOLUTION=1K # Options: 512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # Options: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # Maximum generation attempts during QA loops
```

### 3. การรันด้วย Docker (แนะนำ)

สร้าง Docker image:
```bash
docker-compose build
```

รันเครื่องมือสร้าง:
1.  วางไฟล์ข้อความเรื่องราวของคุณไว้ในโฟลเดอร์ `data/` (เช่น `data/my_story.txt`)
2.  ประมวลผลคอนเทนเนอร์:
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *หมายเหตุ: โฟลเดอร์ `output` จะเต็มไปด้วยผลลัพธ์ที่สร้างขึ้นบนเครื่องโฮสต์ของคุณ*

### 4. การรันบนเครื่องของคุณเอง (Locally)

สร้าง virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

รันแอปพลิเคชัน:
```bash
python main.py --text-file data/my_story.txt --output-dir output/my_project_name
```

## 💡 การใช้งาน

### อาร์กิวเมนต์บรรทัดคำสั่ง (Command Line Arguments)
-   `--text-file`: **(จำเป็น)** เส้นทางไปยังไฟล์ข้อความอินพุตที่มีเรื่องราว
-   `--output-dir`: โฟลเดอร์สำหรับบันทึกทรัพย์สินและภาพประกอบที่สร้างขึ้น (ค่าเริ่มต้น: `output`)
-   `--style-prompt`: พรอมต์เสริมเพื่อกำหนดทิศทางในการตรวจจับสไตล์ในตอนเริ่มต้น (เช่น "Cyberpunk anime", "Oil painting")

### โครงสร้างผลลัพธ์ (Output Structure)
เครื่องมือนี้จะสร้างโครงสร้างโฟลเดอร์ผลลัพธ์ที่เป็นระเบียบ:

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

### โครงสร้าง `data.json`
ไฟล์ `data.json` ทำหน้าที่เป็นข้อมูลแมนิเฟสต์หลัก (central manifest) ของโปรเจกต์

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

## 🧪 การพัฒนาและการทดสอบ

โปรเจกต์นี้ใช้ `pytest` สำหรับการทดสอบ ชุดการทดสอบจะครอบคลุมส่วนของโมเดล การกำหนดค่า การจัดการทรัพย์สิน ความหมายของการแบ่งข้อความของตัววิเคราะห์ และตัวหุ้ม (wrapper) ไคลเอนต์ AI นอกจากนี้ยังทดสอบกลยุทธ์เมื่อระบบล้มเหลว (fallback strategies) อย่างเข้มงวด การจำลองตัวจัดการ PIL IO ขีดจำกัดการทำงานพร้อมกันของ ThreadPool การแมปสคีมาแบบไดนามิก และกลไกการลองใหม่แบบ exponential backoff

วิธีรันการทดสอบ:
```bash
# Activate your virtual environment first
source venv/bin/activate

# Run all tests with coverage reporting
pytest --cov=app --cov-report=term-missing tests/
```

### การทำ Mocking
การทดสอบใช้ `unittest.mock` และ `pytest-mock` เพื่อจำลองการตอบสนองของ Google GenAI API และการทำงานของระบบไฟล์ เพื่อให้แน่ใจว่าการทดสอบจะทำงานได้รวดเร็วและไม่เปลืองโควตา API

## 🏗️ โครงสร้างโปรเจกต์
-   `main.py`: จุดเริ่มต้นและตรรกะการประสานงาน (orchestration logic)
-   `app/`: แพ็กเกจหลัก
    -   `config.py`: การตั้งค่าและการจัดการสภาพแวดล้อม
    -   `core/`: โมดูลตรรกะหลัก
        -   `ai_client.py`: Wrapper สำหรับ Google GenAI SDK
        -   `analyzer.py`: การวิเคราะห์เรื่องราว (การแยกส่วน ฉาก/ตัวละคร/สถานที่)
        -   `asset_manager.py`: จัดการการสร้างและการรวบรวมแคตตาล็อกของทรัพย์สินอ้างอิง
        -   `illustrator.py`: สร้างภาพประกอบฉากสุดท้าย
        -   `models.py`: โมเดลข้อมูล Pydantic
-   `tests/`: ชุดการทดสอบ

## 📜 สัญญาอนุญาต (License)

โปรเจกต์นี้อยู่ภายใต้สัญญาอนุญาต MIT - ดูรายละเอียดเพิ่มเติมได้ในไฟล์ [LICENSE](LICENSE)