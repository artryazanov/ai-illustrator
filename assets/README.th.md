> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator เป็นเครื่องมือทรงพลังที่ออกแบบมาเพื่อสร้างภาพประกอบสำหรับเรื่องราวโดยอัตโนมัติ ซึ่งมีความสอดคล้องและมีคุณภาพสูง โดยใช้โมเดล Gemini ของ Google ทั้งในการวิเคราะห์ข้อความและการสร้างรูปภาพ เครื่องมือนี้จะประมวลผลไฟล์ข้อความของเรื่องราว วิเคราะห์เพื่อทำความเข้าใจสไตล์ภาพ ตัวละคร และสถานที่ จากนั้นจึงสร้างชุดภาพประกอบในรูปแบบภาพยนตร์ (cinematic illustrations)

## 🖼️ ผลงานตัวอย่าง (Showcase)

**นิทานเรื่อง Kolobok**: สำหรับการสาธิตนี้ เราได้ประมวลผลนิทานคลาสสิกเรื่อง "Kolobok" (ก้อนขนมปังกลม) เรื่องราวติดตามก้อนขนมปังอบใหม่ที่มีชีวิตขึ้นมา หลบหนีจากชายและหญิงชรา และกลิ้งหนีเข้าไปในป่า ตลอดการเดินทาง มันร้องเพลงและใช้ไหวพริบเอาชนะกระต่าย หมาป่า และหมี ก่อนที่จะพ่ายแพ้ต่อสุนัขจิ้งจอกเจ้าเล่ห์ในที่สุด

> **พารามิเตอร์การสร้างภาพ:**  
> - **ข้อมูลเรื่องราว (Story Input)**: เนื้อเรื่อง Kolobok  
> - **คำสั่งกำหนดสไตล์ (Style Prompt)**: *"cute and whimsical children's book illustration for toddlers" (ภาพประกอบหนังสือเด็กที่น่ารักและแปลกใหม่สำหรับเด็กวัยเตาะแตะ)*  
> - **โมเดล (Models)**: ข้อความ / ตัวตรวจสอบ (`gemini-3.1-pro-preview`), รูปภาพ (`gemini-3.1-flash-image-preview`)
> - **บริบทความละเอียด (Resolution Context)**: 512px, อัตราส่วนภาพ `1:1`

### การ์ดอ้างอิงตัวละครที่สร้างขึ้น

<p align="center">
  <img src="assets/kolobok/characters/2_old_woman.jpeg" width="16%" alt="Old Woman" title="Old Woman" />
  <img src="assets/kolobok/characters/3_little_round_bun.jpeg" width="16%" alt="Little Round Bun" title="Little Round Bun" />
  <img src="assets/kolobok/characters/4_hare.jpeg" width="16%" alt="Hare" title="Hare" />
  <img src="assets/kolobok/characters/5_the_wolf.jpeg" width="16%" alt="The Wolf" title="The Wolf" />
  <img src="assets/kolobok/characters/6_bear.jpeg" width="16%" alt="Bear" title="Bear" />
  <img src="assets/kolobok/characters/7_the_fox.jpeg" width="16%" alt="The Fox" title="The Fox" />
</p>

### ภาพประกอบฉากที่สร้างขึ้น

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

## ✨ คุณสมบัติ (Features)

-   **การตรวจจับสไตล์อัตโนมัติ (Automatic Style Detection)**: วิเคราะห์ข้อความของเรื่องราวเพื่อกำหนดสไตล์ศิลปะที่เหมาะสมที่สุด และสร้างภาพประกอบที่สอดคล้องกันตามสไตล์นั้น
-   **ความสอดคล้องของตัวละคร (Character Consistency)**:
    -   สกัดคำอธิบายตัวละครและสร้างรูปภาพอ้างอิงของตัวละคร (เต็มตัว)
    -   เก็บรักษารายการตัวละครไว้ใน `output/data.json` อย่างถาวร เพื่อให้แน่ใจว่าตัวละครเดียวกันจะมีลักษณะที่สอดคล้องกันตลอดทั้งเรื่อง
    -   ใช้รูปแบบ **การอ้างอิงที่สะอาด (Clean References)**: การ์ดอ้างอิงตัวละครจะถูกสร้างขึ้นบนพื้นหลังสีขาวล้วนที่แยกส่วนอย่างเคร่งครัด เพื่อป้องกันการปะปนของสภาพแวดล้อมในระหว่างการรวมฉาก
    -   ใช้รูปภาพอ้างอิง (การสร้างแบบ multimodal) เพื่อรักษาลักษณะที่ปรากฏของตัวละครให้คงที่ในฉากต่างๆ
-   **ความสอดคล้องของสถานที่ (Location Consistency)**:
    -   สร้างและแคชรูปภาพอ้างอิงของสถานที่ (ภาพสไตล์ Cinematic)
    -   เก็บรักษารายการสถานที่ไว้ใน `output/data.json` เพื่อนำฉากเดิมกลับมาใช้ใหม่
    -   **การปรับแต่งโควตา (Quota Optimization)**: การจับคู่สถานที่แบบอัจฉริยะช่วยให้แน่ใจว่า API จะสร้างเฉพาะแอสเซทสภาพแวดล้อมสำหรับสถานที่ที่มีการใช้งานจริงในฉากของเรื่องราวเท่านั้น โดยข้ามคำอธิบายพื้นหลังที่ไม่ได้ใช้
-   **การสร้างฉากภาพยนตร์ (Cinematic Scene Generation)**:
    -   แบ่งเรื่องราวออกเป็นฉากเชิงตรรกะอย่างปลอดภัยโดยใช้ Semantic Chunking (รักษาบริบทข้ามส่วนต่างๆ)
    -   ประมวลผลการเรนเดอร์ฉากแบบขนานผ่าน ThreadPool เพื่อการสร้างที่รวดเร็วยิ่งขึ้น
    -   สร้างเฟรมภาพยนตร์ที่สอดคล้องกันเพียงเฟรมเดียวสำหรับแต่ละฉาก (สามารถกำหนดอัตราส่วนภาพได้)
    -   ใช้ประโยชน์จาก **การยึดโยงด้วยข้อความ (Textual Anchoring)** โดยการจับคู่ตัวละครอ้างอิงหลายตัวอย่างชัดเจนผ่านบล็อก `MANDATORY VISUAL DETAILS` ที่มีโครงสร้างอย่างเคร่งครัด เพื่อป้องกันไม่ให้โมเดลสับสนเกี่ยวกับชุดหรือลักษณะเฉพาะระหว่างตัวละคร
-   **ลูป QA แบบ LLM-as-a-Judge และการแก้ไขตนเอง**:
    -   ตรวจสอบรูปภาพที่สร้างขึ้นกับชุดกฎโครงสร้างที่เข้มงวดโดยตรง (เช่น เฟรมเดียว, ข้อจำกัดทางกายวิภาค, ไม่มีข้อความ, ไม่มีขอบ)
    -   หากรูปภาพไม่ผ่านเกณฑ์ (เช่น มีหลายมุมมอง, อวัยวะเกิน, หรือมีกรอบ) คำสั่งการตรวจสอบที่เข้มงวดจะกระตุ้นบล็อกการสร้างใหม่ที่มีข้อจำกัดโดยทันที
    -   **ตัวแก้ไขสไตล์อัจฉริยะ (Intelligent Style Editor)**: นำ AI QA เชิงโปรแกรมมาใช้เพื่อตรวจสอบคำอธิบายรูปแบบข้อความ ป้องกันการแจ้งเตือนที่ผิดพลาด (เช่น การสับสนระหว่างคำต้องห้าม "text" ภายในคำที่อนุญาตอย่าง "texture")
    -   **การรักษาบริบท (Context Preservation)**: ข้อเสนอแนะที่แทรกเข้าไปจะยึดโมเดลไว้แน่นเพื่อรักษาเอกลักษณ์ตัวละครดั้งเดิมและสไตล์ศิลปะไว้ ในขณะที่แก้ไขเฉพาะข้อผิดพลาดทางโครงสร้างที่ตรวจพบเท่านั้น
    -   **การข้ามตัวกรองความปลอดภัย (Safety Filter Bypass)**: ทำความสะอาดข้อบกพร่องจากการ QA ดิบๆ โดยอัตโนมัติผ่านตัวกลาง LLM ที่เป็น "Prompt Engineer" วิธีนี้จะแปลข้อเสนอแนะเชิงลบ (เช่น "ลบลายน้ำ/ลายเซ็น") ให้เป็นคำสั่งเชิงบวกที่มองเห็นได้ชัดเจน ซึ่งจะข้ามตัวกรองการบล็อกตัวสร้างภาพได้อย่างปลอดภัย
    -   นำการตรวจสอบ QA ไปใช้อย่างสม่ำเสมอทั้งกับ **เทมเพลตสไตล์**, **ตัวละคร**, **สถานที่**, และ **ฉาก** เพื่อรักษาความต่อเนื่องของเรื่องราวให้ปราศจากข้อผิดพลาดของภาพ (artifact)
-   **เอาต์พุตที่มีโครงสร้างแบบเนทิฟ (Native Structured Outputs)**:
    -   แทนที่การแยกวิเคราะห์ markdown-JSON ที่เปราะบางด้วยการสนับสนุน `response_schema` ของ Google GenAI ที่เชื่อถือได้ 100% ซึ่งจับคู่โดยตรงกับโมเดล Pydantic
-   **ความเสถียรของ API (API Resilience)**:
    -   จัดการกับขีดจำกัดอัตรา (rate limit), ไทม์เอาต์, และความล้มเหลวของเพย์โหลดของ API อย่างครบถ้วน โดยใช้กลไกการลองใหม่แบบ exponential backoff (`tenacity`)
-   **รองรับ Docker**: ทำงานแบบคอนเทนเนอร์เต็มรูปแบบเพื่อให้ง่ายต่อการปรับใช้และการรัน
-   **การทดสอบที่ครอบคลุม (Comprehensive Testing)**: ครอบคลุมการทดสอบสูงภายใต้ continuous integration (CI) ด้วย Github Actions และ Codecov

## 🛠️ สิ่งที่ต้องมีเบื้องต้น (Prerequisites)

-   **Python 3.12+** (หากรันในเครื่อง/locally)
-   **Docker** และ **Docker Compose** (แนะนำเพื่อแยกสภาพแวดล้อม)
-   **Google Cloud API Key** ที่มีสิทธิ์เข้าถึงโมเดล Gemini (รวมถึงความสามารถในการสร้างรูปภาพ)

## 🚀 การติดตั้งและการตั้งค่า

### 1. โคลน Repository
```bash
git clone git@github.com:artryazanov/ai-illustrator.git
cd ai-illustrator
```

### 2. กำหนดค่า Environment
คัดลอกไฟล์ environment ตัวอย่าง และเพิ่ม API key ของคุณ
```bash
cp .env.example .env
```
เปิดไฟล์ `.env` และกำหนดค่าตัวแปรของคุณ:
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # หรือเวอร์ชันที่รองรับ
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # หรือโมเดล imagen ที่เฉพาะเจาะจง
IMAGE_RESOLUTION=1K # ตัวเลือก: 512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # ตัวเลือก: 1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # จำนวนครั้งสูงสุดในการพยายามสร้างระหว่างลูป QA
```

### 3. รันด้วย Docker (แนะนำ)

สร้าง Docker image:
```bash
docker-compose build
```

รันตัวสร้าง:
1.  วางไฟล์ข้อความเรื่องราวของคุณลงในโฟลเดอร์ `data/` (เช่น `data/my_story.txt`)
2.  เอ็กซีคิวต์คอนเทนเนอร์:
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *หมายเหตุ: โฟลเดอร์ `output` บนเครื่องโฮสต์ของคุณจะถูกเติมเต็มด้วยผลลัพธ์ที่ได้*

### 4. รันในเครื่อง (Running Locally)

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

### อาร์กิวเมนต์ผ่านคอมมานด์ไลน์
-   `--text-file`: **(บังคับ)** เส้นทางไปยังไฟล์ข้อความอินพุตที่มีเรื่องราวอยู่
-   `--output-dir`: โฟลเดอร์สำหรับบันทึกแอสเซทและภาพประกอบที่สร้างขึ้น (ค่าเริ่มต้น: `output`)
-   `--style-prompt`: (ตัวเลือกเสริม) คำสั่งเพื่อเป็นแนวทางในการตรวจจับสไตล์เริ่มต้น (เช่น "Cyberpunk anime", "Oil painting")

### โครงสร้างของผลลัพธ์ (Output Structure)
เครื่องมือนี้จะสร้างโฟลเดอร์เอาต์พุตแบบแบนราบที่เป็นระเบียบ:

```
output/
├── characters/             # แอสเซทตัวละคร
│   └── 1_character_name.jpeg
├── locations/              # แอสเซทสถานที่
│   └── 1_location_name.jpeg
├── illustrations/          # ภาพประกอบฉากในเรื่อง
│   └── 1_sunny_park_scene.jpeg
├── data.json               # ข้อมูล manifest รวม (สไตล์, ตัวละคร, สถานที่, ภาพประกอบ)
└── style_templates/        # รูปภาพตั้งต้นของสไตล์ที่สร้างขึ้น
    ├── style_reference_fullbody.jpg   # การอ้างอิงสไตล์ตัวละครแบบไดนามิก
    └── bg_location.jpg                # พื้นหลังที่เป็นกลางแบบไดนามิกสำหรับสถานที่
```

### โครงสร้างของ `data.json`
ไฟล์ `data.json` ทำหน้าที่เป็น manifest กลางสำหรับโปรเจกต์

```json
{
  "style_prompt": "คำอธิบายของสไตล์ภาพ...",
  "characters": [
    {
      "id": 1,
      "name": "ชื่อตัวละคร",
      "original_name": "ชื่อเดิมจากข้อความ",
      "description": "คำอธิบายลักษณะท่าทาง...",
      "full_body_path": "output/characters/1_character_name.jpeg",
      "generation_prompt": "คำสั่งแบบเต็มที่ใช้ในการสร้าง..."
    }
  ],
  "locations": [
    {
      "id": 1,
      "name": "ชื่อสถานที่",
      "original_name": "ชื่อเดิมจากข้อความ",
      "description": "คำอธิบายลักษณะท่าทาง...",
      "reference_image_path": "output/locations/1_location_name.jpeg",
      "generation_prompt": "คำสั่งแบบเต็มที่ใช้ในการสร้าง..."
    }
  ],
  "illustrations": [
    {
      "scene_id": 1,
      "story_segment": "ข้อความเดิมของฉาก...",
      "name": "sunny_park_scene",
      "location": {
        "id": 1,
        "name": "ชื่อสถานที่"
      },
      "characters": [
        {
          "id": 1,
          "name": "ชื่อตัวละคร",
          "full_body_path": "output/characters/1_character_name.jpeg"
        }
      ],
      "illustration_path": "output/illustrations/1_sunny_park_scene.jpeg",
      "generation_prompt": "คำสั่งแบบเต็มที่ใช้ในการสร้าง..."
    }
  ]
}
```

## 🧪 การพัฒนาและการทดสอบ (Development & Testing)

โปรเจกต์นี้ใช้ `pytest` สำหรับการทดสอบ ชุดการทดสอบครอบคลุมถึงโมเดล, การกำหนดค่า, การจัดการแอสเซท, ความหมายของการแบ่งข้อความของเครื่องมือวิเคราะห์, และ AI client wrapper นอกจากนี้ยังทดสอบกลยุทธ์เมื่อเกิดข้อผิดพลาด (fallback), PIL IO handler แบบจำลอง (mock), ขีดจำกัดการทำงานพร้อมกันของ ThreadPool, การจับคู่ schema แบบไดนามิก, และกลไกการลองใหม่แบบ exponential backoff อย่างเข้มงวด

วิธีรันการทดสอบ:
```bash
# เปิดใช้งาน virtual environment ของคุณก่อน
source venv/bin/activate

# รันการทดสอบทั้งหมดพร้อมรายงาน coverage
pytest --cov=app --cov-report=term-missing tests/
```

### การจำลอง (Mocking)
การทดสอบใช้ `unittest.mock` และ `pytest-mock` เพื่อจำลองการตอบกลับของ Google GenAI API และการทำงานของระบบไฟล์ ทำให้มั่นใจได้ว่าการทดสอบจะมีความรวดเร็วและไม่สิ้นเปลืองโควตาของ API

## 🏗️ โครงสร้างโปรเจกต์ (Project Structure)
-   `main.py`: จุดเริ่มต้นและตรรกะการประสานงานหลัก
-   `app/`: แพ็กเกจหลัก
    -   `config.py`: การตั้งค่าและการจัดการ environment
    -   `core/`: โมดูลตรรกะที่สำคัญ
        -   `ai_client.py`: Wrapper สำหรับ Google GenAI SDK
        -   `analyzer.py`: การวิเคราะห์เรื่องราว (การสกัด ฉาก/ตัวละคร/สถานที่)
        -   `asset_manager.py`: จัดการการสร้างและทำรายการแอสเซทอ้างอิง
        -   `illustrator.py`: สร้างภาพประกอบฉากในท้ายที่สุด
        -   `models.py`: โมเดลข้อมูล Pydantic
-   `tests/`: ชุดการทดสอบ

## 📜 ลิขสิทธิ์ (License)

โปรเจกต์นี้ได้รับอนุญาตภายใต้ MIT License - ดูรายละเอียดได้ที่ไฟล์ [LICENSE](LICENSE)