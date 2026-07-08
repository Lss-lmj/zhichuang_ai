# 编译原理教学演示 · 统一视觉与交互规范

> 本规范用于确保 13 个 HTML 页面（1 首页 + 12 个课节）风格一致、可离线运行、面向课堂展示。

## 1. 主题定位
- **场景**：大学"编译原理"课程课堂投屏演示。
- **风格**：现代科技感 + 学术严谨感；深色/浅色双主色，配高对比强调色。
- **交互**：以"下一步 / 上一步 / 重置 / 自动播放"为主；不依赖后端；单文件即可运行。

## 2. 配色（CSS 变量）
```css
:root {
  --bg: #0f1226;               /* 主背景（深空蓝）*/
  --bg-soft: #171a35;          /* 卡片背景 */
  --bg-code: #0a0c1c;          /* 代码块背景 */
  --fg: #e7ebff;               /* 主文字 */
  --fg-dim: #a0a8d0;           /* 次要文字 */
  --line: #2a2f55;             /* 分隔线/边框 */
  --accent: #6ee7ff;           /* 强调 · 青蓝（当前步骤/高亮）*/
  --accent-2: #ffb86b;         /* 强调 · 橙（活跃状态）*/
  --success: #7ee787;          /* 成功 · 绿 */
  --danger: #ff6b8a;           /* 危险 · 粉红（错误/移除）*/
  --purple: #b78cff;           /* 装饰 · 紫（次要高亮）*/
  --shadow: 0 10px 30px rgba(0,0,0,0.35);
  --radius: 14px;
  --radius-sm: 8px;
}
```

## 3. 字体
- 界面：`-apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif`
- 代码：`"JetBrains Mono", "Fira Code", Menlo, Consolas, monospace`

## 4. 布局骨架
每个主题页面统一使用如下三段式结构：

```
┌─────────────────────────────────────────────┐
│ Header：主题标题 + 返回首页按钮               │
├────────────┬────────────────────────────────┤
│ 左侧       │ 右侧                            │
│ 讲解卡片   │ 可视化画布（SVG/DOM 动画）        │
│ (30%)     │ (70%)                          │
├────────────┴────────────────────────────────┤
│ Footer：上一步 / 步骤指示器 / 下一步 / 重置    │
└─────────────────────────────────────────────┘
```

- 讲解卡片：随当前步骤同步高亮/切换文字；标出"要点""定义""注意"三类徽章。
- 可视化画布：以 SVG 为主，节点用 `<g>` 分组，动画使用 CSS transition + JS 切换 class。

## 5. 交互约定
- 键盘：`←` 上一步；`→` 下一步；`Space` 播放/暂停；`R` 重置。
- 步骤指示器：小圆点，当前步骤填充为 `--accent`。
- 自动播放节奏：默认 1600ms/步，可通过右下角速度按钮切换 0.5×/1×/2×。
- 所有动画使用 `prefers-reduced-motion` 兼容降级。

## 6. 组件命名（各页共用 class）
- `.demo-shell` 外壳容器
- `.demo-header` 顶部
- `.demo-main` 主区
- `.panel-explain` 左侧讲解
- `.panel-stage` 右侧舞台
- `.demo-controls` 底部控制条
- `.step-dot` / `.step-dot.active`
- `.badge` / `.badge--tip` / `.badge--warn` / `.badge--def`
- `.node`（图节点）/ `.node.active` / `.node.done`
- `.edge` / `.edge.active`
- `.token` / `.token.current` / `.token.consumed`

## 7. 文件组织
```
compiler-demos/
├── index.html                    (导航首页)
├── DESIGN_SPEC.md
└── pages/
    ├── 01-lexical.html           (词法分析：正则→NFA→DFA)
    ├── 02-parsing.html           (语法分析：LL/LR)
    ├── 06-ast.html               (AST 构建：解析树→抽象语法树)
    ├── 07-scope.html             (作用域规则：声明绑定与遮蔽)
    ├── 03-semantic.html          (语义分析与符号表)
    ├── 08-type-check.html        (类型检查：AST 类型传播)
    ├── 04-ir.html                (中间代码生成)
    ├── 09-control-flow.html      (控制流生成：if/while→标签与基本块)
    ├── 05-optimize.html          (代码优化)
    ├── 10-expression-compiler.html (表达式编译器综合实验)
    ├── 11-error-recovery.html    (错误恢复与继续分析)
    └── 12-compiler-regression.html (编译器测试与回归验证)
```

## 8. 无依赖
- 全部使用原生 HTML/CSS/JS + 内联 SVG；不引入任何 CDN；离线可跑。
- 中文优先展示；关键术语标注英文缩写。
