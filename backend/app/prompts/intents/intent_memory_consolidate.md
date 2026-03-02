# Intent Instruction: MEMORY_CONSOLIDATE

用户主要意图：系统后台任务，整理、合并、清洗现有的记忆。

## 目标
检查输入的记忆列表，执行以下操作：
1. **去重 (Deduplicate)**: 合并语义重复的条目。
2. **去冲突 (Resolve Conflict)**: 若有矛盾（如“喜欢红色”和“讨厌红色”），**保留最新的信息**，或标记为冲突。
3. **合并 (Merge)**: 将碎片信息合并为完整画像（如“喜欢苹果”+“喜欢香蕉” -> “喜欢水果，特别是苹果和香蕉”）。
4. **归纳 (Generalize)**: 从多个具体事实中提炼出通用模式（例如：多次提到使用 Python 库 -> “用户是 Python 开发者”）。
5. **归档 (Archive)**: 识别已完成的项目或过时的目标，将其状态更新为“已完成”或“已归档”（例如：“项目 X 进行中” -> “项目 X 已于 2025 年完成”）。
6. **失效检查 (Prune)**: 删除明显错误或不再相关的信息。

## 输入格式
一个包含现有记忆的 JSON 列表。

## 输出格式（JSON）
**重要：content 字段必须使用中文描述。**

Strict JSON object with changes:
```json
{
  "to_delete": [1, 5], // IDs to remove
  "to_add": [
    {
      "content": "用户非常喜欢水果，特别是苹果和香蕉。",
      "category": "preference"
    },
    {
      "content": "用户是 Python 全栈开发者。",
      "category": "fact"
    }
  ],
  "to_update": [
    {
      "id": 3,
      "content": "项目 Jarvis v5.3 已完成，目前正在开发 v5.4。",
      "category": "project"
    }
  ]
}
```
