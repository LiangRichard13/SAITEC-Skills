# SAITEC-Skills

MCP (Model Context Protocol) 服务，为 Agent 提供 AIGC 检测与 LLM 评估能力。所有工具通过 SAITEC Core 代理 API（`/api/v1/skills/`）访问，经过鉴权与数据库事务管理。

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

或使用 conda：

```bash
conda run -n skills pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# SAITEC Core 代理 API 地址
export CORE_API_BASE=http://127.0.0.1:8000

# API 鉴权密钥（后端中间件通过 X-API-Key 头鉴权）
export SAITEC_API_KEY=你的API密钥
```

### 3. 启动 MCP 服务

```bash
python mcp_server/server.py
```

## 工具列表

共 29 个 MCP tools，分为 7 个模块。

### Text Detect（文本 AIGC 检测）

| 工具 | 说明 |
|------|------|
| `detect_text(text, method, threshold, language, task_name)` | 检测单条文本是否为 AI 生成 |
| `batch_detect_texts(items, method, threshold, task_name)` | 批量检测多条文本 |
| `get_text_task(task_id)` | 查询文本检测任务详情 |
| `get_text_task_artifacts(task_id)` | 获取文本检测任务产物 |

### Image Detect（图片 AIGC 检测）

| 工具 | 说明 |
|------|------|
| `detect_image(image_uri, method, threshold, return_visuals)` | 检测单张图片是否为 AI 生成 |
| `batch_detect_images(items, method)` | 批量检测多张图片 |
| `get_image_task(task_id)` | 查询图片检测任务详情 |
| `get_image_task_artifacts(task_id)` | 获取图片检测任务产物 |

### Video Detect（视频 AIGC 检测）

| 工具 | 说明 |
|------|------|
| `detect_video(video_uri, method, threshold)` | 检测单个视频是否为 AI 生成 |
| `batch_detect_videos(items)` | 批量检测多个视频 |
| `get_video_task(task_id)` | 查询视频检测任务详情 |
| `get_video_task_artifacts(task_id)` | 获取视频检测任务产物 |

### Safety Eval（LLM 安全评测）

| 工具 | 说明 |
|------|------|
| `create_safety_eval(task_name, model_name, judge_model_name, ...)` | 创建 LLM 安全评测任务 |
| `inject_safety_credentials(env_name, api_key, overwrite)` | 注入运行时凭证 |
| `get_safety_task(task_id)` | 查询安全评测任务详情 |
| `get_safety_task_artifacts(task_id)` | 获取安全评测任务产物 |

### Corpus Safety Eval（语料安全评测）

| 工具 | 说明 |
|------|------|
| `create_corpus_safety_eval(task_name, texts, dataset, ...)` | 创建语料安全评测任务 |
| `inject_corpus_credentials(env_name, api_key, overwrite)` | 注入运行时凭证 |
| `get_corpus_safety_task(task_id)` | 查询语料安全评测任务详情 |
| `get_corpus_safety_task_artifacts(task_id)` | 获取语料安全评测任务产物 |

### General Eval（通用 LLM 能力评测）

| 工具 | 说明 |
|------|------|
| `create_general_eval(task_name, model_name, judge_model_name, ...)` | 创建通用能力评测任务 |
| `inject_general_credentials(env_name, api_key, overwrite)` | 注入运行时凭证 |
| `get_general_task(task_id)` | 查询通用评测任务详情 |
| `get_general_task_artifacts(task_id)` | 获取通用评测任务产物 |

### File Manage（文件管理）

| 工具 | 说明 |
|------|------|
| `upload_file(file_path, file_type)` | 上传本地文件（自动 base64 编码） |
| `download_file(file_id)` | 下载文件 |
| `list_files(skip, limit)` | 列出用户私有文件 |
| `list_task_files(task_id)` | 列出任务产物文件 |

## 安全说明

- 所有工具请求均携带 `X-API-Key` header，密钥从环境变量 `SAITEC_API_KEY` 读取
- 请求发往 SAITEC Core 代理 API（`/api/v1/skills/`），不直接访问内部后端服务
- 代理 API 层负责鉴权、用户归属验证和数据库事务管理

## 目录结构

```
├── README.md
├── requirements.txt
├── agent_sops/                     # Agent 思考指南（SOP）
│   ├── aigc_detect_sop.md
│   └── llm_eval_sop.md
└── mcp_server/
    ├── server.py                  # MCP 服务入口
    └── api_tools/                 # 各模块工具实现
        ├── __init__.py
        ├── text_detect_tools.py
        ├── image_detect_tools.py
        ├── video_detect_tools.py
        ├── safety_eval_tools.py
        ├── corpus_safety_eval_tools.py
        ├── general_eval_tools.py
        └── file_manage_tools.py
```
