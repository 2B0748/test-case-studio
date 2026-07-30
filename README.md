<p align="center">
  <img src="https://img.shields.io/badge/%E7%B1%BB%E5%9E%8B-Claude%20Code%20Skill-blue?style=for-the-badge" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/%E9%A2%86%E5%9F%9F-%E8%BD%AF%E4%BB%B6%E6%B5%8B%E8%AF%95-green?style=for-the-badge" alt="软件测试">
  <img src="https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E4%B8%AD%E6%96%87-red?style=for-the-badge" alt="中文">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License">
</p>

<h1 align="center">🧪 测试用例工作室（Test Case Studio）</h1>

<p align="center">
  <strong>需求 → 测试点 → 用例 → 评审 · 一站式测试用例设计 Skill</strong>
</p>

<p align="center">
  面向软件测试工程师的 <b>AI 驱动</b>测试用例设计工具<br>
  覆盖 <b>功能 · 接口(API) · 性能 · 安全 · 兼容性</b> 全类型<br>
  支持 <b>Markdown + Excel</b> 双格式输出，可直接导入禅道 / TestRail / Jira
</p>

---

## 📖 这是什么？

**测试用例工作室** 是一个 [Claude Code](https://claude.ai/code) 的 Skill 插件，把软件测试中"需求理解 → 测试点拆解 → 用例设计编写 → 用例评审"四个环节串成**标准化的 AI 工作流**。

你只需要提供 PRD、需求文档、接口文档或用户故事，Skill 就会自动按专业方法轮产出测试点清单、完整用例表和评审报告——不再从零手写，不再遗漏边界场景。

---

## ✨ 核心能力

| 能力 | 说明 |
|------|------|
| 🧩 **四阶段工作流** | 需求理解 → 测试设计 → 用例编写 → 用例评审，一气呵成 |
| 🎯 **八种设计方法** | 等价类、边界值、判定表、因果图、状态迁移、场景法、错误推测、正交试验 |
| 📋 **五类用例覆盖** | 功能用例 · 接口用例 · 性能用例 · 安全用例 · 兼容用例 |
| 🔍 **八维评审体系** | 覆盖度 / 正确性 / 可执行性 / 独立性 / 颗粒度 / 可追溯 / 优先级 / 去重 |
| 📦 **双格式输出** | Markdown 表格 + Excel(.xlsx)，一键导入禅道 / TestRail / Jira |
| 🧠 **设计方法自动匹配** | 根据输入特征自动推荐等价类+边界值、判定表、场景法等最佳方法组合 |

---

## 🗂️ 项目结构

```
test-case-studio/
├── SKILL.md                          # 🔑 Skill 主指令文件（四阶段完整流程）
├── README.md                         # 📄 项目说明（本文件）
├── references/
│   ├── methodology.md                # 📚 测试设计方法库 + 字段定义 + 优先级标准
│   ├── prompts.md                    # 📝 可导出到外部工具的提示词模板
│   └── review-checklist.md           # ✅ 用例评审检查单（八维度 + 严重度 + 结论判定）
├── assets/
│   ├── test-case-template.md         # 📋 Markdown 用例模板（表头 + 示例）
│   └── test-case-template.xlsx       # 📊 Excel 用例模板（可导入禅道 / TestRail）
└── scripts/
    └── md_to_xlsx.py                 # 🔧 Markdown 用例表 → Excel / CSV 转换器（零依赖）
```

---

## 🚀 快速开始

### 前置要求

- 安装 [Claude Code](https://docs.anthropic.com/zh-CN/docs/claude-code/overview)（VS Code / JetBrains 插件或 CLI）
- （可选）Python 3 + openpyxl，用于 Excel 导出：`pip install openpyxl`

### 安装 Skill

**方式一：下载安装**

```bash
# 1. 克隆本仓库到 Claude Code 的 skills 目录
git clone https://github.com/<your-username>/test-case-studio.git ~/.claude/skills/test-case-studio
```

**方式二：手动安装**

将本项目文件夹放入 Claude Code 的 skills 目录，或通过 VS Code 插件设置中指定 Skill 路径。

### 使用方式

在 Claude Code 对话中直接触发：

```
帮我把这份 PRD 拆成测试点
```

```
根据接口文档写一份完整的 API 测试用例
```

```
评审这份用例的覆盖度
```

```
帮我检查登录模块的安全测试是否充分
```

Skill 会自动识别意图并进入对应的执行阶段。

---

## 🔄 工作流详解

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  阶段 1     │ ──▶│  阶段 2     │ ──▶│  阶段 3     │ ──▶│  阶段 4     │
│  需求理解   │    │  测试设计   │    │  用例编写   │    │  用例评审   │
│  测试点拆解 │    │  方法选择   │    │  格式输出   │    │  自检清单   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     │                   │                  │                  │
     ▼                   ▼                  ▼                  ▼
 测试点清单          方法+用例展开      Markdown 用例表      评审报告
 (模块·类型·优先级)  (等价类·边界值…)  (标准字段·双格式)    (通过/打回·修订)
```

### 各阶段要点

**阶段 1 · 需求理解**：提炼功能清单、识别业务规则与约束、标注风险与优先级，产出测试点清单（粒度 = 一类验证意图）。

**阶段 2 · 测试设计**：为每个测试点自动匹配最佳设计方法——等价类+边界值几乎是标配，多条件走判定表，流程走场景法，状态机走状态迁移。

**阶段 3 · 用例编写**：按标准字段（编号/模块/标题/类型/方法/优先级/前置条件/步骤/数据/预期/追溯）输出，标题规范为 `【类型】【预期】动作+对象`。

**阶段 4 · 用例评审**：八维度逐条核对，输出评审结论（通过/有条件通过/打回）+ 问题清单 + 覆盖度统计 + 修订后用例。

---

## 📦 输出格式

### Markdown 用例表

标准表格格式，字段齐全，可直接在对话中查看或导出为 `.md` 文件。

### Excel 导出

```bash
# 先让 Skill 生成 Markdown 用例文件，然后：
python scripts/md_to_xlsx.py outputs/用例.md --out outputs/用例.xlsx
```

- 自动按 `##` 章节分 Sheet
- 单元格内 `<br>` 自动转为 Excel 换行
- 表头深色背景 + 冻结首行
- 列宽自适应（中文按 2 字符计）
- 无 openpyxl 时自动回退为 UTF-8 CSV（Excel 可直接打开）

---

## 🎓 设计方法论

| 方法 | 适用场景 | 示例 |
|------|----------|------|
| 等价类划分 + 边界值 | 输入有范围/格式约束 | 密码长度 6-20 位 |
| 判定表 / 因果图 | 多条件组合逻辑 | 优惠券叠加规则 |
| 状态迁移 | 状态流转明显 | 订单：待支付→已支付→已发货 |
| 场景法 | 业务流程/用户旅程 | 注册→登录→下单→支付 |
| 错误推测 | 历史缺陷/经验 | 特殊字符、超长输入、并发重复提交 |
| 正交试验 / Pairwise | 参数组合爆炸 | 浏览器 × OS × 分辨率兼容矩阵 |

> 详见 [references/methodology.md](references/methodology.md)

---

## ✅ 评审标准

| 维度 | 检查要点 |
|------|----------|
| 覆盖度 | 需求点 100% 覆盖，正向/反向/边界/异常/分支齐全 |
| 正确性 | 预期结果明确、可判定、可观测 |
| 可执行性 | 步骤可复现，前置条件和测试数据齐备 |
| 独立性 | 用例间无依赖，可单独执行 |
| 颗粒度 | 一个用例验证一个点 |
| 可追溯 | 需求追溯字段可回溯到原始需求 |
| 优先级 | P0/P1 划分合理（单模块 P0 ≤ 20%） |
| 去重 | 无冗余重复用例 |

> 详见 [references/review-checklist.md](references/review-checklist.md)

---

## 🤝 适用场景

- ✅ 新需求上线前的测试用例设计
- ✅ 接口文档产出后的 API 测试用例编写
- ✅ 安全审计前的安全测试场景覆盖
- ✅ 性能压测前的场景设计与指标定义
- ✅ 已有用例的质量评审与覆盖度检查
- ✅ 用例格式标准化，批量导入测试管理平台

---

## 📄 许可证

MIT License — 自由使用、修改和分发。

---

## ⭐ Star 历史

如果这个项目对你有帮助，欢迎点个 **Star** ⭐ 让更多测试同行看到！

---

<p align="center">
  <sub>Built with ❤️ for QA Engineers | Powered by Claude Code</sub>
</p>
