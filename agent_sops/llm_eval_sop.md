# LLM 评估 SOP

## 触发条件

当用户需要评估 LLM 能力、查看排行榜或对比多个模型时调用。

## 调用工具

- **单模型评估**: `evaluate_llm(model_name: str, tasks: list[str])`
- **模型对比**: `compare_llms(model_names: list[str], task: str)`

## 评估维度

| 维度 | 说明 |
|------|------|
| `math` | 数学推理能力 |
| `code` | 代码生成能力 |
| `reasoning` | 逻辑推理能力 |
| `language` | 语言理解能力 |

## 结果展示

- 数值评分（0-100）
- 支持生成雷达图、柱状图对比
- 可导出 CSV 报告
