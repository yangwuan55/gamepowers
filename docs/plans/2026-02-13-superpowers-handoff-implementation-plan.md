# Superpowers Handoff Execution Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 基于 GamePowers 交接包在实现代码库内按 ECS 契约执行开发，并通过 bd 跟踪任务状态。

**Architecture:** 以 `generated-handoff-20260213-114941.md` 为执行入口，先进行计划拆解，再按 TDD 执行任务，最后验证 ECS 约束与文档追溯关系。每个实现任务都绑定对应设计文档，状态统一写入 bd。

**Tech Stack:** superpowers skills、bd CLI、目标代码库语言栈

---

### Task 1: 加载交接输入并拆解实现批次

**Files:**
- Read: `docs/gamepowers/handoffs/generated-handoff-20260213-114941.md`
- Read: `docs/gamepowers/index/task-doc-map.yaml`
- Read: `docs/gamepowers/index/bd-task-map-20260213-114941.json`

**Step 1: Write the failing test**

```bash
bd ready --limit 20
```

**Step 2: Run test to verify it fails**

Run: `bd ready --limit 20`
Expected: 至少有一个可执行任务。

**Step 3: Write minimal implementation**

- 选定本批次可执行任务。
- 将任务按“设计类/技术类”拆分。

**Step 4: Run test to verify it passes**

Run: `bd show <task-id>`
Expected: 可看到任务描述中包含文档引用。

**Step 5: Commit**

```bash
# 该阶段通常为计划动作，不要求代码提交。
```

### Task 2: 按 TDD 执行首批实现任务

**Files:**
- Modify: `目标代码库中的实现文件`
- Test: `目标代码库中的测试文件`

**Step 1: Write the failing test**

```bash
# 在目标代码库执行单测，先观察失败
```

**Step 2: Run test to verify it fails**

Run: `pytest ...` 或 `npm test ...`
Expected: 失败且失败原因与待实现行为相关。

**Step 3: Write minimal implementation**

- 实现最小变更让测试通过。

**Step 4: Run test to verify it passes**

Run: `pytest ...` 或 `npm test ...`
Expected: 首批任务相关测试通过。

**Step 5: Commit**

```bash
git add <changed-files>
git commit -m "feat: implement first handoff batch under tdd"
```

### Task 3: 验证 ECS 契约与追溯关系

**Files:**
- Read: `docs/gamepowers/ecs/system-schedule.md`
- Read: `docs/gamepowers/ecs/event-flow.md`
- Read: `docs/gamepowers/ecs/performance-budget.md`

**Step 1: Write the failing test**

```bash
# 针对 ECS 约束添加或执行现有验证测试
```

**Step 2: Run test to verify it fails**

Run: `pytest ecs_tests/...` 或同等命令
Expected: 未满足 ECS 约束时失败。

**Step 3: Write minimal implementation**

- 修正系统调度顺序、事件处理、性能预算埋点。

**Step 4: Run test to verify it passes**

Run: `pytest ecs_tests/...`
Expected: 全部通过。

**Step 5: Commit**

```bash
git add <changed-files>
git commit -m "feat: enforce ecs contract from gamepowers handoff"
```

### Task 4: 更新 bd 与交付总结

**Files:**
- Modify: `docs/gamepowers/handoffs/generated-handoff-20260213-114941.md`（必要时）
- Create: `docs/gamepowers/handoffs/superpowers-execution-summary.md`

**Step 1: Write the failing test**

```bash
bd ready --limit 20
```

**Step 2: Run test to verify it fails**

Run: `bd ready --limit 20`
Expected: 若仍有未完成项则显示。

**Step 3: Write minimal implementation**

- 关闭已完成的 bd 任务。
- 更新交付总结（实现范围、测试证据、剩余风险）。

**Step 4: Run test to verify it passes**

Run: `bd ready --limit 20`
Expected: 本轮目标任务无未完成项。

**Step 5: Commit**

```bash
git add docs/gamepowers/handoffs/superpowers-execution-summary.md
git commit -m "docs: summarize superpowers execution from handoff"
```
