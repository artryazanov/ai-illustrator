> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator เป็นเครื่องมือทรงพลังที่ออกแบบมาเพื่อสร้างภาพประกอบสำหรับเรื่องราวต่างๆ อย่างต่อเนื่องและมีคุณภาพสูงโดยอัตโนมัติ โดยใช้โมเดล Gemini ของ Google สำหรับทั้งการวิเคราะห์ข้อความและการสร้างรูปภาพ มันจะประมวลผลไฟล์ข้อความของเรื่องราว วิเคราะห์เพื่อทำความเข้าใจสไตล์ภาพ ตัวละคร และสถานที่ จากนั้นจึงสร้างชุดภาพประกอบที่สวยงามราวกับภาพยนตร์

## 🖼️ ผลงานตัวอย่าง

**นิทานโคโลบก (Kolobok)**: สำหรับการสาธิตนี้ เราได้ประมวลผลนิทานคลาสสิกเรื่อง "Kolobok" (ก้อนขนมปังกลมๆ) เรื่องราวเกี่ยวกับก้อนขนมปังอบใหม่ๆ ที่มีชีวิต หนีจากตาและยาย แล้วกลิ้งเข้าไปในป่า ระหว่างทางมันได้ร้องเพลงและใช้ความฉลาดเอาชนะกระต่าย หมาป่า และหมี ก่อนที่จะถูกสุนัขจิ้งจอกเจ้าเล่ห์หลอกกินในที่สุด

> **พารามิเตอร์การสร้าง:**  
> - **ข้อมูลเรื่องราว (Story Input)**: เนื้อเรื่องของ Kolobok  
> - **พรอมต์สไตล์ (Style Prompt)**: *"cute and whimsical children's book illustration for toddlers"*  
> - **โมเดล (Models)**: ข้อความ / ผู้ตรวจสอบ (`gemini-3.1-pro-preview`), รูปภาพ (`gemini-3.1-flash-image-preview`)
> - **บริบทความละเอียด (Resolution Context)**: 512px, อัตราส่วนภาพ `1:1`

### การ์ดอ้างอิงตัวละครที่สร้างขึ้น

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

## ✨ คุณสมบัติ

-   **การตรวจจับสไตล์อัตโนมัติ**: วิเคราะห์ข้อความในเรื่องราวเพื่อกำหนดสไตล์ศิลปะที่เหมาะสมที่สุด และสร้างภาพประกอบที่มีความสอดคล้องกันตามสไตล์นั้น
-   **ความสอดคล้องของตัวละคร**:
    -   ดึงคำอธิบายตัวละครและสร้างรูปภาพอ้างอิงสำหรับตัวละคร (เต็มตัว)
    -   เก็บแคตตาล็อกตัวละครแบบถาวรไว้ใน `output/data.json` เพื่อให้แน่ใจว่าตัวละครเดียวกันจะมีรูปลักษณ์ที่สอดคล้องกันตลอดทั้งเรื่อง
    -   ใช้รูปแบบ **Clean References**: การ์ดอ้างอิงตัวละครจะถูกสร้างขึ้นบนพื้นหลังสีขาวบริสุทธิ์แบบแยกเดี่ยวอย่างเคร่งครัด เพื่อป้องกันไม่ให้สภาพแวดล้อมปะปนเข้ามาในระหว่างการรวมฉาก
    -   ใช้รูปภาพอ้างอิง (การสร้างแบบ multimodal) เพื่อรักษาลักษณะของตัวละครให้คงที่ในฉากต่างๆ
-   **ความสอดคล้องของสถานที่**:
    -   สร้างและแคชรูปภาพอ้างอิงสถานที่ (ภาพสไตล์ภาพยนตร์)
    -   เก็บแคตตาล็อกสถานที่ไว้ใน `output/data.json` เพื่อนำฉากกลับมาใช้ใหม่
    -   **การปรับแต่งโควต้า (Quota Optimization)**: การจับคู่สถานที่อย่างชาญฉลาดช่วยให้มั่นใจได้ว่า API จะสร้างเฉพาะทรัพยากรสภาพแวดล้อมสำหรับสถานที่ที่มีการใช้งานจริงในฉากของเรื่องราวเท่านั้น โดยข้ามคำอธิบายพื้นหลังที่ไม่ได้ใช้งาน
-   **การสร้างฉากแบบภาพยนตร์**:
    -   แบ่งเรื่องราวออกเป็นฉากๆ อย่างสมเหตุสมผลและปลอดภัยโดยใช้ Semantic Chunking (รักษาบริบทข้ามส่วนต่างๆ)
    -   เรนเดอร์ฉากแบบขนานผ่าน ThreadPool เพื่อการสร้างที่รวดเร็วยิ่งขึ้น
    -   สร้างเฟรมภาพยนตร์แบบรวมเป็นหนึ่งเดียวสำหรับแต่ละฉาก (สามารถกำหนดค่าอัตราส่วนภาพได้)
    -   ใช้ **Textual Anchoring** โดยการแมปการอ้างอิงตัวละครหลายตัวอย่างชัดเจนผ่านบล็อก `MANDATORY VISUAL DETAILS` ที่มีโครงสร้างเข้มงวด เพื่อป้องกันไม่ให้โมเดลสับสนเกี่ยวกับชุดแต่งกายหรือลักษณะเด่นระหว่างตัวละคร
-   **LLM-as-a-Judge QA Loop และการแก้ไขตัวเอง (Self-Correction)**:
    -   ตรวจสอบรูปภาพที่สร้างขึ้นกับชุดกฎเชิงโครงสร้างที่เข้มงวดในตัว (เช่น เฟรมเดียว, ข้อจำกัดทางกายวิภาค, ไม่มีข้อความ, ไม่มีเส้นขอบ)
    -   หากรูปภาพไม่ผ่านเกณฑ์ (เช่น มีหลายมุมมอง, แขนขาเกินมา หรือมีเส้นขอบเฟรม) พรอมต์ตรวจสอบที่เข้มงวดจะเรียกใช้บล็อกการสร้างใหม่ที่มีการควบคุมในทันที
    -   **Intelligent Style Editor**: นำระบบ QA แบบ AI เชิงโปรแกรมมาใช้เพื่อตรวจสอบคำอธิบายสไตล์ของข้อความ ช่วยป้องกันการเตือนที่ผิดพลาด (เช่น การสับสนระหว่างคำที่ถูกแบน "text" กับคำที่อนุญาตอย่าง "texture")
    -   **การรักษาบริบท**: ฟีดแบ็กที่ป้อนเข้าไปจะช่วยยึดโยงโมเดลให้รักษาเอกลักษณ์ดั้งเดิมของตัวละครและสไตล์ศิลปะไว้ ในขณะที่แก้ไขเฉพาะข้อผิดพลาดทางโครงสร้างที่ตรวจพบเท่านั้น
    -   **การข้ามตัวกรองความปลอดภัย (Safety Filter Bypass)**: ทำความสะอาดข้อผิดพลาดดิบจาก QA โดยอัตโนมัติผ่านโมเดล LLM ตัวกลาง "Prompt Engineer" วิธีนี้จะแปลฟีดแบ็กเชิงลบ (เช่น "ลบลายน้ำ/ลายเซ็น") ให้เป็นพรอมต์เชิงบวกที่มีภาพชัดเจน ซึ่งสามารถข้ามตัวกรองการบล็อกของตัวสร้างรูปภาพได้อย่างปลอดภัย
    -   ใช้การตรวจสอบ QA อย่างสม่ำเสมอในทุกส่วน ทั้ง **แม่แบบสไตล์ (Style Templates)**, **ตัวละคร**, **สถานที่**, และ **ฉาก** เพื่อรักษาความสอดคล้องของเรื่องราวให้ไร้ข้อบกพร่อง
-   **Native Structured Outputs**:
    -   แทนที่การแยกวิเคราะห์ markdown-JSON ที่เปราะบางด้วยการรองรับ `response_schema` ของ Google GenAI ที่เชื่อถือได้ 100% ซึ่งจับคู่โดยตรงกับโมเดล Pydantic
-   **ความเสถียรของ API**:
    -   จัดการกับขีดจำกัดอัตรา (rate limits) ของ API, การหมดเวลา, และข้อผิดพลาดของข้อมูล (payload failures) อย่างเต็มรูปแบบโดยใช้กลไกการลองใหม่แบบ exponential backoff (`tenacity`)
-   **รองรับ Docker**: จัดการในรูปแบบคอนเทนเนอร์อย่างเต็มรูปแบบเพื่อให้ง่ายต่อการปรับใช้และการทำงาน
-   **การทดสอบที่ครอบคลุม**: ครอบคลุมการทดสอบสูงภายใต้ระบบ continuous integration ด้วย Github Actions & Codecov

## 🛠️ ข้อกำหนดเบื้องต้น

-   **Python 3.12+** (หากทำงานบนเครื่องแบบ local)
-   **Docker** และ **Docker Compose** (แนะนำเพื่อแยกสภาพแวดล้อมการทำงาน)
-   **Google Cloud API Key** ที่สามารถเข้าถึงโมเดล Gemini ได้ (รวมถึงความสามารถในการสร้างรูปภาพ)

## 🚀 การติดตั้งและตั้งค่า

### 1. โคลน Repository
```bash
git clone git@github.com:artryazanov/ai-illustrator.git
cd ai-illustrator
```

### 2. กำหนดค่าสภาพแวดล้อม
คัดลอกไฟล์สภาพแวดล้อมตัวอย่าง และเพิ่ม API key ของคุณ
```bash
cp .env.example .env
```
เปิด `.env` และตั้งค่าตัวแปรของคุณ:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # หรือเวอร์ชันที่เข้ากันได้
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # หรือโมเดลสร้างภาพ (imagen model) ที่เฉพาะเจาะจง
IMAGE_RESOLUTION=1K # ตัวเลือก: 512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # ตัวเลือก: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # จำนวนครั้งสูงสุดในการพยายามสร้างระหว่างลูป QA
```

### 3. การรันด้วย Docker (แนะนำ)

บิลด์ Docker image:
```bash
docker-compose build
```

รันตัวสร้าง:
1.  วางไฟล์ข้อความเรื่องราวของคุณในไดเรกทอรี `data/` (เช่น `data/my_story.txt`)
2.  รันคอนเทนเนอร์:
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *หมายเหตุ: ไดเรกทอรี `output` จะมีผลลัพธ์ปรากฏขึ้นบนเครื่องโฮสต์ของคุณ*

### 4. การรันบนเครื่องแบบ Local

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
-   `--text-file`: **(จำเป็น)** เส้นทางไปยังไฟล์ข้อความที่นำเข้า ซึ่งบรรจุเนื้อเรื่องอยู่
-   `--output-dir`: ไดเรกทอรีสำหรับบันทึกทรัพยากรที่สร้างขึ้นและภาพประกอบ (ค่าเริ่มต้น: `output`)
-   `--style-prompt`: พรอมต์ทางเลือก (Optional) สำหรับแนะนำการตรวจจับสไตล์เริ่มต้น (เช่น "Cyberpunk anime", "Oil painting")

### โครงสร้างผลลัพธ์ (Output Structure)
เครื่องมือนี้จะสร้างไดเรกทอรีผลลัพธ์แบบแบนราบที่เป็นระเบียบ:

```
output/
├── characters/             # ทรัพยากรตัวละคร
│   └── 1_character_name.jpeg
├── locations/              # ทรัพยากรสถานที่
│   └── 1_location_name.jpeg
├── illustrations/          # ภาพประกอบฉากในท้ายที่สุด
│   └── 1_sunny_park_scene.jpeg
├── data.json               # ข้อมูลรวมแบบ manifest (สไตล์, ตัวละคร, สถานที่, ภาพประกอบ)
└── style_templates/        # รูปภาพฐานที่สร้างขึ้นสำหรับสไตล์
    ├── style_reference_fullbody.jpg   # การอ้างอิงสไตล์ตัวละครแบบไดนามิก
    └── bg_location.jpg                # พื้นหลังที่เป็นกลางแบบไดนามิกสำหรับสถานที่
```

### โครงสร้างไฟล์ `data.json`
ไฟล์ `data.json` ทำหน้าที่เป็นข้อมูลแมนิเฟสต์กลาง (central manifest) สำหรับโปรเจ็กต์

```json
{
  "style_prompt": "คำอธิบายสไตล์ภาพ...",
  "characters": [
    {
      "id": 1,
      "name": "Character Name",
      "original_name": "ชื่อดั้งเดิมจากข้อความ",
      "description": "คำอธิบายภาพลักษณ์...",
      "full_body_path": "output/characters/1_character_name.jpeg",
      "generation_prompt": "พรอมต์ทั้งหมดที่ใช้ในการสร้าง..."
    }
  ],
  "locations": [
    {
      "id": 1,
      "name": "Location Name",
      "original_name": "ชื่อดั้งเดิมจากข้อความ",
      "description": "คำอธิบายภาพลักษณ์...",
      "reference_image_path": "output/locations/1_location_name.jpeg",
      "generation_prompt": "พรอมต์ทั้งหมดที่ใช้ในการสร้าง..."
    }
  ],
  "illustrations": [
    {
      "scene_id": 1,
      "story_segment": "ข้อความต้นฉบับของฉาก...",
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
      "generation_prompt": "พรอมต์ทั้งหมดที่ใช้ในการสร้าง..."
    }
  ]
}
```

## 🧪 การพัฒนาและการทดสอบ

โปรเจ็กต์นี้ใช้ `pytest` สำหรับการทดสอบ ชุดการทดสอบครอบคลุมถึงโมเดล, การตั้งค่า, การจัดการทรัพยากร, ความหมายของการแยกข้อความของ analyzer, และ wrapper ของ AI ไคลเอ็นต์ มีการทดสอบกลยุทธ์การทำงานสำรอง (fallback), mocked PIL IO handlers, ข้อจำกัดการทำงานพร้อมกันของ ThreadPool, การจับคู่สคีมาแบบไดนามิก และกลไกการลองใหม่แบบ exponential backoff อย่างเข้มงวด

วิธีรันการทดสอบ:
```bash
# เปิดใช้งาน virtual environment ของคุณก่อน
source venv/bin/activate

# รันการทดสอบทั้งหมดพร้อมการรายงาน coverage
pytest --cov=app --cov-report=term-missing tests/
```

### การ Mocking
การทดสอบใช้ `unittest.mock` และ `pytest-mock` เพื่อจำลองการตอบสนองของ Google GenAI API และการทำงานของระบบไฟล์ เพื่อให้มั่นใจว่าการทดสอบมีความรวดเร็วและไม่สิ้นเปลืองโควต้า API

## 🏗️ โครงสร้างโปรเจ็กต์
-   `main.py`: จุดเริ่มต้นโปรแกรม (Entry point) และตรรกะการประสานงาน
-   `app/`: แพ็กเกจหลัก
    -   `config.py`: การตั้งค่าและการจัดการสภาพแวดล้อม
    -   `core/`: โมดูลตรรกะที่สำคัญ
        -   `ai_client.py`: Wrapper สำหรับ Google GenAI SDK
        -   `analyzer.py`: การวิเคราะห์เรื่องราว (การดึงข้อมูล ฉาก/ตัวละคร/สถานที่)
        -   `asset_manager.py`: จัดการการสร้างและทำแคตตาล็อกทรัพยากรอ้างอิง
        -   `illustrator.py`: สร้างภาพประกอบฉากในท้ายที่สุด
        -   `models.py`: โมเดลข้อมูล Pydantic
-   `tests/`: ชุดการทดสอบ

## 📜 ลิขสิทธิ์ (License)

โปรเจ็กต์นี้ใช้ไลเซนส์ MIT - ดูรายละเอียดเพิ่มเติมได้ในไฟล์ [LICENSE](LICENSE)