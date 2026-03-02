# Policy: Reflection Attribution Rules (Deterministic First)

本文件定义反思引擎的“优先级最高”的归因规则。反思引擎必须：
1) **先匹配以下规则**得到 stage + prompt_targets（确定性归因）
2) 只有在无规则命中时，才允许使用 LLM 做补充归因（并必须标注低置信度）

## Stage 枚举（固定）
- router
- context_assembler
- reminder_policy
- memory_retrieval
- long_history_search
- image_analysis
- file_import
- response_format
- safety_policy
- tool_or_skill
- unknown

## Prompt targets（固定路径集合）
- system/system_core.md
- modes/mode_expert.md
- modes/mode_work.md
- modes/mode_life.md
- modes/mode_learn.md
- intents/intent_qa_knowledge.md
- intents/intent_task_execution.md
- intents/intent_planning.md
- intents/intent_decision_support.md
- intents/intent_social_chat.md
- intents/intent_learning_tutor.md
- intents/intent_management.md
- intents/intent_reflection_evolution.md
- policies/reminder_block_policy.md
- policies/context_budget_policy.md
- policies/tool_action_plan_policy.md
- policies/next_actions_policy.md
- policies/file_import_policy.md
- policies/prompt_evolution_policy.md
- policies/reflection_attribution_rules.md

---

## 规则 1：提醒块缺失（最重要）
触发条件：
- 注入/系统日志显示存在 due/overdue reminders
- 且 assistant 输出中未出现 "【提醒】"

归因：
- stage = reminder_policy
- prompt_targets 必须包含：
  - policies/reminder_block_policy.md
- 可选追加：
  - system/system_core.md

---

## 规则 2：输出太长 / 用户要求简短
触发条件（任一）：
- 用户说：太长/啰嗦/简短点/只要结论/别展开
- 或系统检测：assistant 字符数 > LENGTH_THRESHOLD

归因：
- stage = response_format
- prompt_targets：
  - system/system_core.md（必须）
  - + 当次 primary_intent 对应 intents/intent_*.md（可选）

---

## 规则 3：规划缺少 DoD / 不够可执行
触发条件（任一）：
- 用户要求计划/路线图/拆解，但回复缺里程碑/任务/下一步/DoD
- 用户反馈：不够具体/没有可执行步骤/没有里程碑

归因：
- stage = response_format
- prompt_targets：
  - intents/intent_planning.md（必须）
- 可选追加：
  - modes/mode_work.md（处于 WORK 时）

---

## 规则 4：回答跑题 / 未聚焦当前问题
触发条件（任一）：
- 用户反馈：没回答/跑题
- 自动检查：assistant 未回应 query 的关键实体/问句类型

归因：
- stage = context_assembler
- prompt_targets：
  - policies/context_budget_policy.md
  - system/system_core.md

---

## 规则 5：模式不合适（语气/风格不匹配）
触发条件：
- 用户反馈：太正式/太冷/别教育我/别这么专业

归因：
- stage = router
- prompt_targets：
  - 对应 modes/mode_*.md（按当次 primary_mode）
  - system/system_core.md（可选收敛）

---

## 规则 6：外部动作未走 ActionPlan/未确认（例如日历）
触发条件（任一）：
- assistant 声称“已经创建/已经发送/已经修改系统”
- 或没有输出【ActionPlan】但请求涉及外部动作

归因：
- stage = tool_or_skill
- prompt_targets：
  - policies/tool_action_plan_policy.md（必须）
  - system/system_core.md（可选）

---

## 规则 7：文件/截图理解错误或过度推断
触发条件：
- 用户反馈：文件不是这个意思/你读错了
- 或 assistant 引用不存在的文件内容

归因：
- stage = file_import（或 image_analysis）
- prompt_targets：
  - policies/file_import_policy.md（必须）
  - system/system_core.md（可选）

---

## 规则 8：安全/隐私问题
触发条件：
- assistant 要求敏感信息或引导高风险动作无确认

归因：
- stage = safety_policy
- prompt_targets：
  - system/system_core.md（必须）

---

## 无规则命中兜底
- stage = unknown
- prompt_targets：system/system_core.md
- LLM 可给低置信备选归因（<=2），必须说明证据不足。
