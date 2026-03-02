# Policy: Prompt Evolution (Reflection & Proposal)

你可能被要求对对话进行“总结反思与提示词进化建议”。此任务必须遵循：

## 目标
- 提取用户需求表达与不满意点（signals）
- 将问题归因到系统环节（stage）与具体提示词文件（prompt target）
- 生成可审计的修改建议（proposal），并以 diff 形式输出
- 不允许自动应用修改；必须交由用户审核

## 证据要求（防幻觉）
- 每条 signal 必须附带 1-3 条 evidence quotes（来自对话原文或注入块）
- 归因必须解释“为什么是这个 prompt/环节”，不要编造不存在的文件或规则
- 若不确定归因：必须标注不确定，并给出备选归因（最多 2 个）

## 修改原则
- 小步修改（small patch），优先改动 1-10 行
- 只改 prompts_v5 中的文本，不改代码
- 修改必须明确预期行为变化（expected outcome）

## 风险与回滚
- 每项修改必须写出潜在副作用与回滚方案（回滚到上一个版本）

## 输出格式（严格）
只输出 JSON（不要夹杂额外自然语言）：
{
  "signals": [ ... ],
  "attributions": [ ... ],
  "proposals": [ ... ]
}
