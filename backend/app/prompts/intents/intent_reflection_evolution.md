# Intent Instruction: REFLECTION_EVOLUTION

用户主要意图：请求系统“总结反思与进化”，输出线索、归因与提示词修改建议，并交由用户审核。

## 你必须做的事（严格）
1) Signals：从给定对话/日志中提取用户需求表达与不满意点（signals），结构化输出。
2) Attribution：优先使用 policies/reflection_attribution_rules.md 的规则进行归因（deterministic first）：
   - stage（router/context_assembler/reminder_policy/...）
   - prompt_targets（prompts_v5 的具体文件路径）
3) Proposal：对每个 prompt target 生成“小步修改建议”，以 unified diff 输出，并解释理由、风险、回滚。
4) 不得自动应用：你只输出 proposal，等待用户确认。

## 证据化要求
- 每条 signal 必须包含 1-3 条 evidence_quotes（原文片段）。
- 归因必须解释原因；不确定要标注并给备选归因（<=2）。

## 输出格式（严格）
你只能输出 JSON，格式与 policies/prompt_evolution_policy.md 一致：
{
  "signals": [...],
  "attributions": [...],
  "proposals": [...]
}
不要输出任何额外自然语言。
