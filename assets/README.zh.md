> 🌐 **Languages:** [English](https://github.com/artryazanov/ai-illustrator/blob/main/README.md) | [Русский](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ru.md) | [ไทย](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.th.md) | [中文](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.zh.md) | [Español](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.es.md) | [العربية](https://github.com/artryazanov/ai-illustrator/blob/main/assets/README.ar.md)

# AI Illustrator

[![Tests](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/tests.yml)
[![Linting](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml/badge.svg)](https://github.com/artryazanov/ai-illustrator/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/artryazanov/ai-illustrator/branch/main/graph/badge.svg)](https://codecov.io/gh/artryazanov/ai-illustrator)
![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI Illustrator 是一款强大的工具，旨在使用 Google 的 Gemini 模型（用于文本分析和图像生成）为故事自动生成连贯、高质量的插图。它会处理故事文本文件，对其进行分析以理解视觉风格、角色和场景，然后生成一系列具有电影感画面的插图。

## 🖼️ 展示

**《小圆面包》（Kolobok）的故事**：在本次演示中，我们处理了经典童话故事《小圆面包》。故事讲述了一个刚烤好的圆面包复活后，从老爷爷和老奶奶身边逃走，一路滚进了森林。在旅途中，它一边唱歌一边智胜了野兔、狼和熊，但最终却被一只狡猾的狐狸骗了。

> **生成参数：**  
> - **故事输入**：《小圆面包》文本  
> - **风格提示词**：*"cute and whimsical children's book illustration for toddlers"（可爱奇幻的幼儿绘本插图）*  
> - **模型**：文本/验证（`gemini-3.1-pro-preview`），图像（`gemini-3.1-flash-image-preview`）
> - **分辨率上下文**：512px，`1:1` 宽高比

### 生成的角色参考卡

<p align="center">
  <img src="assets/kolobok/characters/2_old_woman.jpeg" width="16%" alt="Old Woman" title="Old Woman" />
  <img src="assets/kolobok/characters/3_little_round_bun.jpeg" width="16%" alt="Little Round Bun" title="Little Round Bun" />
  <img src="assets/kolobok/characters/4_hare.jpeg" width="16%" alt="Hare" title="Hare" />
  <img src="assets/kolobok/characters/5_the_wolf.jpeg" width="16%" alt="The Wolf" title="The Wolf" />
  <img src="assets/kolobok/characters/6_bear.jpeg" width="16%" alt="Bear" title="Bear" />
  <img src="assets/kolobok/characters/7_the_fox.jpeg" width="16%" alt="The Fox" title="The Fox" />
</p>

### 生成的场景插图

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

## ✨ 特性

-   **自动风格检测**：分析故事文本以确定最合适的艺术风格，并根据该风格生成连贯的插图。
-   **角色一致性**：
    -   提取角色描述并生成参考角色图像（全身）。
    -   在 `output/data.json` 中维护一个持久的角色目录，以确保同一角色在整个故事中的外观保持一致。
    -   使用 **纯净参考（Clean References）** 模式：角色参考卡严格在隔离的纯白背景上生成，以防止在场景整合时发生环境色溢出。
    -   使用参考图像（多模态生成）保持角色在不同场景中的外观稳定。
-   **场景一致性**：
    -   生成并缓存场景参考图像（电影风格镜头）。
    -   在 `output/data.json` 中维护一个场景目录以便复用设定。
    -   **配额优化**：智能场景匹配功能确保 API 仅为故事场景中实际存在的地点生成环境资产，跳过未使用的背景描述。
-   **电影级场景生成**：
    -   使用语义分块（Semantic Chunking）安全地将故事拆分为逻辑场景（跨区块保留上下文）。
    -   通过线程池（ThreadPool）并行化场景渲染，以加快生成速度。
    -   为每个场景生成具有连贯电影感的单帧画面（长宽比可配置）。
    -   利用 **文本锚定（Textual Anchoring）** 技术，通过严格结构化的 `MANDATORY VISUAL DETAILS` （强制视觉细节）块，显式映射多角色参考，防止模型混淆不同角色之间的服装或特征。
-   **大语言模型裁判（LLM-as-a-Judge）质检循环与自我修正**：
    -   原生根据严格的结构规则集（如：单帧、解剖学约束、无文字、无边框）验证生成的图像。
    -   如果图像未通过验证（例如出现多角度视图、多余的肢体或框架边框），严格的验证提示词会立即触发受限的重新生成机制。
    -   **智能风格编辑器**：实现程序化的 AI 质检以验证文本风格描述，防止误报（例如在允许的词 "texture" 中混淆了被禁用的词 "text"）。
    -   **上下文保留**：注入的反馈强力锚定模型，在专注于修复指出的结构错误的同时，保留原始的角色身份和艺术风格。
    -   **安全过滤器绕过**：通过中间的“提示词工程师（Prompt Engineer）” LLM 流程，自动净化原始的质检失败信息。将负面反馈（例如“移除水印/签名”）转化为积极的、视觉清晰的提示词，从而安全地绕过图像生成器的拦截过滤器。
    -   将质检验证统一应用于**风格模板**、**角色**、**场景**和**插图画面**，以维持一个连贯且无瑕疵的故事叙述。
-   **原生结构化输出**：
    -   使用 100% 可靠的 Google GenAI `response_schema` 支持（直接映射到 Pydantic 模型），取代了脆弱的 Markdown-JSON 解析。
-   **API 弹性**：
    -   使用指数退避重试机制（`tenacity`）全面处理 API 速率限制、超时和载荷失败。
-   **Docker 支持**：完全容器化，便于部署和执行。
-   **全面的测试**：在 Github Actions 和 Codecov 持续集成下保持高测试覆盖率。

## 🛠️ 环境要求

-   **Python 3.12+** （如果在本地运行）
-   **Docker** & **Docker Compose** （推荐用于环境隔离）
-   拥有 Gemini 模型（包含图像生成功能）访问权限的 **Google Cloud API 密钥**。

## 🚀 安装与设置

### 1. 克隆仓库
```bash
git clone git@github.com:artryazanov/ai-illustrator.git
cd ai-illustrator
```

### 2. 配置环境
复制环境示例文件并添加您的 API 密钥。
```bash
cp .env.example .env
```
打开 `.env` 并设置您的变量：
```ini
GEMINI_API_KEY=your_api_key_here
TEXT_MODEL_NAME=gemini-3.1-pro-preview # 或兼容模型
IMAGE_MODEL_NAME=gemini-3.1-flash-image-preview # 或特定 imagen 模型
IMAGE_RESOLUTION=1K # 选项：512, 1K, 2K, 4K
IMAGE_ASPECT_RATIO=1:1 # 选项：1:1, 1:4, 1:8, 2:3, 3:2, 3:4, 4:1, 4:3, 4:5, 5:4, 8:1, 9:16, 16:9, 21:9
MAX_RETRIES=4 # 质检循环期间的最大生成尝试次数
```

### 3. 使用 Docker 运行（推荐）

构建 Docker 镜像：
```bash
docker-compose build
```

运行生成器：
1.  将您的故事文本文件放入 `data/` 目录中（例如：`data/my_story.txt`）。
2.  执行容器：
    ```bash
    docker-compose run app --text-file data/my_story.txt --output-dir output/my_project_name
    ```
    *注意：宿主机上的 `output` 目录将被生成的输出结果填充。*

### 4. 本地运行

创建虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate
```

安装依赖项：
```bash
pip install -r requirements.txt
```

运行应用程序：
```bash
python main.py --text-file data/my_story.txt --output-dir output/my_project_name
```

## 💡 使用方法

### 命令行参数
-   `--text-file`：**(必填)** 包含故事的输入文本文件的路径。
-   `--output-dir`：保存生成的资产和插图的目录（默认：`output`）。
-   `--style-prompt`：可选提示词，用于引导初始风格检测（例如："Cyberpunk anime", "Oil painting"）。

### 输出目录结构
该工具会创建一个井然有序的平面输出目录：

```
output/
├── characters/             # 角色资产
│   └── 1_character_name.jpeg
├── locations/              # 场景资产
│   └── 1_location_name.jpeg
├── illustrations/          # 最终场景插图
│   └── 1_sunny_park_scene.jpeg
├── data.json               # 统一清单（风格、角色、场景、插图）
└── style_templates/        # 生成的风格基础图片
    ├── style_reference_fullbody.jpg   # 动态角色风格参考
    └── bg_location.jpg                # 用于场景的动态中性背景
```

### `data.json` 结构
`data.json` 文件是项目的核心清单。

```json
{
  "style_prompt": "视觉风格的描述...",
  "characters": [
    {
      "id": 1,
      "name": "角色名称",
      "original_name": "文本中的原始名称",
      "description": "视觉描述...",
      "full_body_path": "output/characters/1_character_name.jpeg",
      "generation_prompt": "所使用的完整生成提示词..."
    }
  ],
  "locations": [
    {
      "id": 1,
      "name": "场景名称",
      "original_name": "文本中的原始名称",
      "description": "视觉描述...",
      "reference_image_path": "output/locations/1_location_name.jpeg",
      "generation_prompt": "所使用的完整生成提示词..."
    }
  ],
  "illustrations": [
    {
      "scene_id": 1,
      "story_segment": "场景的原始文本...",
      "name": "sunny_park_scene",
      "location": {
        "id": 1,
        "name": "场景名称"
      },
      "characters": [
        {
          "id": 1,
          "name": "角色名称",
          "full_body_path": "output/characters/1_character_name.jpeg"
        }
      ],
      "illustration_path": "output/illustrations/1_sunny_park_scene.jpeg",
      "generation_prompt": "所使用的完整生成提示词..."
    }
  ]
}
```

## 🧪 开发与测试

本项目使用 `pytest` 进行测试。测试套件涵盖了模型、配置、资产管理、分析器文本拆分语义以及 AI 客户端封装。它严格测试了回退策略、模拟 PIL IO 处理器、ThreadPool 并发限制、动态 Schema 映射以及指数退避重试机制。

运行测试：
```bash
# 首先激活您的虚拟环境
source venv/bin/activate

# 运行所有测试并生成覆盖率报告
pytest --cov=app --cov-report=term-missing tests/
```

### 模拟 (Mocking)
测试使用 `unittest.mock` 和 `pytest-mock` 来模拟 Google GenAI API 的响应和文件系统操作，从而确保测试运行快速且不会消耗 API 配额。

## 🏗️ 项目结构
-   `main.py`：入口点及编排逻辑。
-   `app/`：核心包。
    -   `config.py`：配置与环境变量管理。
    -   `core/`：关键逻辑模块。
        -   `ai_client.py`：Google GenAI SDK 的封装层。
        -   `analyzer.py`：故事分析（提取场景/角色/地点）。
        -   `asset_manager.py`：管理参考资产的创建和编目。
        -   `illustrator.py`：生成最终的场景插图。
        -   `models.py`：Pydantic 数据模型。
-   `tests/`：测试套件。

## 📜 许可证

本项目基于 MIT 许可证开源 - 详情请参阅 [LICENSE](LICENSE) 文件。